import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_db
from models import Category, Provider

router = APIRouter(tags=["categories"])
logger = logging.getLogger("backend.routers.categories")

LOGOS_DIR = Path("data/logos")
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

CATEGORY_PRESETS = [
    "OpenAI", "Anthropic", "Google", "Deepseek",
    "阿里", "百度", "字节", "智谱", "月之暗面",
]


class CategoryCreate(BaseModel):
    name: str
    api_base_url: str = ""
    api_usage_path: str = "/v1/usage"
    api_balance_path: str | None = None
    tp_base_url: str = ""
    tp_usage_path: str = "/v1/usage"
    currency_symbol: str = "CNY"
    models: list[str] = []


class CategoryUpdate(BaseModel):
    name: str | None = None
    api_base_url: str | None = None
    api_usage_path: str | None = None
    api_balance_path: str | None = None
    tp_base_url: str | None = None
    tp_usage_path: str | None = None
    currency_symbol: str | None = None
    models: list[str] | None = None


def _category_dict(c: Category) -> dict:
    return {
        "id": c.id, "name": c.name,
        "api_base_url": c.api_base_url,
        "api_usage_path": c.api_usage_path,
        "api_balance_path": c.api_balance_path,
        "tp_base_url": c.tp_base_url,
        "tp_usage_path": c.tp_usage_path,
        "currency_symbol": c.currency_symbol,
        "models": c.models or [],
        "logo_path": c.logo_path,
    }


@router.get("/categories/presets")
async def get_presets():
    return CATEGORY_PRESETS


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.name))
    return [_category_dict(c) for c in result.scalars().all()]


@router.post("/categories")
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    cat = Category(
        name=data.name,
        api_base_url=data.api_base_url,
        api_usage_path=data.api_usage_path,
        api_balance_path=data.api_balance_path,
        tp_base_url=data.tp_base_url,
        tp_usage_path=data.tp_usage_path,
        currency_symbol=data.currency_symbol,
        models=data.models,
    )
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    logger.info("Category created | id=%s name=%s", cat.id, cat.name)
    return _category_dict(cat)


@router.put("/categories/{category_id}")
async def update_category(category_id: int, data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    for field in ("name", "api_base_url", "api_usage_path", "api_balance_path",
                  "tp_base_url", "tp_usage_path", "currency_symbol", "models"):
        val = getattr(data, field, None)
        if val is not None:
            setattr(cat, field, val)

    await db.commit()
    logger.info("Category updated | id=%s", category_id)
    return _category_dict(cat)


@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.execute(
        select(Provider).where(Provider.category_id == category_id)
    )
    prov_result = await db.execute(
        select(Provider).where(Provider.category_id == category_id)
    )
    for p in prov_result.scalars().all():
        p.category_id = None

    # Delete logo file if exists
    if cat.logo_path:
        logo_file = Path(cat.logo_path)
        if logo_file.exists():
            logo_file.unlink()

    await db.delete(cat)
    await db.commit()
    logger.info("Category deleted | id=%s", category_id)
    return {"message": "Category deleted"}


@router.post("/categories/{category_id}/logo")
async def upload_logo(category_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    # Validate extension
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 20MB")

    # Ensure logos directory exists
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old logo if exists
    if cat.logo_path:
        old_file = Path(cat.logo_path)
        if old_file.exists():
            old_file.unlink()

    # Save new file
    filename = f"{category_id}{ext}"
    file_path = LOGOS_DIR / filename
    file_path.write_bytes(content)

    # Update database
    cat.logo_path = f"data/logos/{filename}"
    await db.commit()

    logger.info("Logo uploaded | category_id=%s file=%s", category_id, filename)
    return {"logo_path": cat.logo_path}


@router.get("/categories/{category_id}/logo")
async def get_logo(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat or not cat.logo_path:
        raise HTTPException(status_code=404, detail="Logo not found")

    file_path = Path(cat.logo_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Logo file not found")

    return FileResponse(file_path)


@router.delete("/categories/{category_id}/logo")
async def delete_logo(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    if cat.logo_path:
        file_path = Path(cat.logo_path)
        if file_path.exists():
            file_path.unlink()
        cat.logo_path = None
        await db.commit()

    return {"message": "Logo deleted"}
