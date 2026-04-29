import httpx
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_db
from models import Provider
from services.crypto import encrypt, decrypt, mask_key
from services.collector import collect_usage
from services.scheduler import register_job, remove_job, reschedule_job

router = APIRouter(tags=["providers"])
logger = logging.getLogger("backend.routers.providers")


# ── Schemas ────────────────────────────

class ProviderCreate(BaseModel):
    name: str
    api_key: str
    base_url: str
    usage_api_path: str = "/v1/usage"
    balance_api_path: str | None = None
    models: list[str] = []
    usage_mapping: dict | None = None
    balance_mapping: dict | None = None
    currency_symbol: str = "CNY"
    interval_seconds: int = 0
    billing_mode: str = "api"
    monthly_fee: float | None = None
    sub_start_date: str | None = None


class ProviderUpdate(BaseModel):
    name: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    usage_api_path: str | None = None
    balance_api_path: str | None = None
    models: list[str] | None = None
    usage_mapping: dict | None = None
    balance_mapping: dict | None = None
    currency_symbol: str | None = None
    interval_seconds: int | None = None
    billing_mode: str | None = None
    monthly_fee: float | None = None
    sub_start_date: str | None = None


class ProviderResponse(BaseModel):
    model_config = {"populate_by_name": True}

    id: int
    name: str
    api_key: str
    base_url: str
    usage_api_path: str
    balance_api_path: str | None = None
    last_balance: float | None = None
    models: list
    usage_mapping: dict | None = None
    balance_mapping: dict | None = None
    currency_symbol: str = "CNY"
    interval_seconds: int
    billing_mode: str = "api"
    monthly_fee: float | None = None
    sub_start_date: str | None = None
    created_at: str


class TestApiRequest(BaseModel):
    base_url: str
    api_key: str
    api_path: str


class ProviderTestApiRequest(BaseModel):
    api_path: str


def _provider_response(p: Provider) -> ProviderResponse:
    return ProviderResponse(
        id=p.id,
        name=p.name,
        api_key=mask_key(decrypt(p.api_key)),
        base_url=p.base_url,
        usage_api_path=p.usage_api_path,
        balance_api_path=p.balance_api_path,
        last_balance=p.last_balance,
        models=p.models or [],
        usage_mapping=p.usage_mapping,
        balance_mapping=p.balance_mapping,
        currency_symbol=p.currency_symbol,
        interval_seconds=p.interval_seconds,
        billing_mode=p.billing_mode,
        monthly_fee=p.monthly_fee,
        sub_start_date=p.sub_start_date,
        created_at=p.created_at.isoformat(),
    )


# ── Routes ─────────────────────────────

@router.get("/providers", response_model=list[ProviderResponse])
async def list_providers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).where(Provider.deleted == False).order_by(Provider.created_at.desc())
    )
    return [_provider_response(p) for p in result.scalars().all()]


@router.post("/providers", response_model=ProviderResponse)
async def create_provider(data: ProviderCreate, db: AsyncSession = Depends(get_db)):
    if data.interval_seconds > 0 and data.interval_seconds < 10:
        raise HTTPException(status_code=422, detail="interval_seconds must be 0 (manual) or >= 10")

    provider = Provider(
        name=data.name,
        api_key=encrypt(data.api_key),
        base_url=data.base_url,
        usage_api_path=data.usage_api_path,
        balance_api_path=data.balance_api_path,
        models=data.models,
        usage_mapping=data.usage_mapping,
        balance_mapping=data.balance_mapping,
        currency_symbol=data.currency_symbol,
        interval_seconds=data.interval_seconds,
        billing_mode=data.billing_mode,
        monthly_fee=data.monthly_fee,
        sub_start_date=data.sub_start_date,
    )
    db.add(provider)
    await db.commit()
    await db.refresh(provider)

    if provider.interval_seconds > 0:
        register_job(provider.id, provider.interval_seconds, _scheduled_collect)

    logger.info("Provider created | provider_id=%s name=%s interval=%s", provider.id, provider.name, provider.interval_seconds)
    return _provider_response(provider)


@router.put("/providers/{provider_id}", response_model=ProviderResponse)
async def update_provider(provider_id: int, data: ProviderUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id, Provider.deleted == False)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        logger.warning("Provider not found for update | provider_id=%s", provider_id)
        raise HTTPException(status_code=404, detail="Provider not found")

    old_interval = provider.interval_seconds

    for field in ("name", "base_url", "usage_api_path", "balance_api_path",
                  "models", "usage_mapping", "balance_mapping", "currency_symbol",
                  "billing_mode", "monthly_fee", "sub_start_date"):
        val = getattr(data, field, None)
        if val is not None:
            setattr(provider, field, val)
    if data.api_key is not None:
        decrypted = decrypt(provider.api_key)
        if data.api_key != mask_key(decrypted):
            provider.api_key = encrypt(data.api_key)
    if data.interval_seconds is not None:
        if data.interval_seconds > 0 and data.interval_seconds < 10:
            raise HTTPException(status_code=422, detail="interval_seconds must be 0 (manual) or >= 10")
        provider.interval_seconds = data.interval_seconds

    await db.commit()
    await db.refresh(provider)

    if provider.interval_seconds != old_interval:
        reschedule_job(provider.id, provider.interval_seconds, _scheduled_collect)

    logger.info("Provider updated | provider_id=%s name=%s", provider.id, provider.name)
    return _provider_response(provider)


@router.delete("/providers/{provider_id}")
async def delete_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id, Provider.deleted == False)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        logger.warning("Provider not found for delete | provider_id=%s", provider_id)
        raise HTTPException(status_code=404, detail="Provider not found")

    provider.deleted = True
    remove_job(provider_id)
    await db.commit()
    logger.info("Provider deleted | provider_id=%s name=%s", provider_id, provider.name)
    return {"message": "Provider deleted"}


@router.post("/providers/test-api")
async def test_api(req: TestApiRequest):
    logger.info("API test requested | base_url=%s api_path=%s", req.base_url, req.api_path)
    url = f"{req.base_url.rstrip('/')}{req.api_path}"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, headers={"Authorization": f"Bearer {req.api_key}"})
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            return {
                "status_code": resp.status_code,
                "body": body,
            }
    except Exception as e:
        return {"status_code": -1, "body": str(e)}


@router.post("/providers/{provider_id}/test-api")
async def test_api_for_provider(provider_id: int, req: ProviderTestApiRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id, Provider.deleted == False)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        logger.warning("Provider not found for test | provider_id=%s", provider_id)
        raise HTTPException(status_code=404, detail="Provider not found")

    decrypted_key = decrypt(provider.api_key)
    url = f"{provider.base_url.rstrip('/')}{req.api_path}"
    logger.info("Provider-scoped API test | provider_id=%s base_url=%s api_path=%s", provider_id, provider.base_url, req.api_path)
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, headers={"Authorization": f"Bearer {decrypted_key}"})
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            return {
                "status_code": resp.status_code,
                "body": body,
            }
    except Exception as e:
        return {"status_code": -1, "body": str(e)}


@router.post("/providers/{provider_id}/collect")
async def trigger_collect(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id, Provider.deleted == False)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        logger.warning("Provider not found for collect | provider_id=%s", provider_id)
        raise HTTPException(status_code=404, detail="Provider not found")

    logger.info("Manual collection triggered | provider_id=%s", provider_id)
    try:
        usage_result, balance_result = await collect_usage(provider, db)
        logger.info("Manual collection completed | provider_id=%s usage=%s balance=%s",
                     provider_id, usage_result.get("status"), balance_result.get("status") if balance_result else "N/A")
        return {"usage": usage_result, "balance": balance_result}
    except Exception as e:
        logger.error("Manual collection failed | provider_id=%s error=%s", provider_id, e)
        return {"usage": {"status": "error", "message": str(e)}, "balance": None}


# ── Scheduler callback ─────────────────

async def _scheduled_collect(provider_id: int):
    from database import AsyncSessionLocal
    from sqlalchemy import select as sa_select

    async with AsyncSessionLocal() as db:
        result = await db.execute(sa_select(Provider).where(Provider.id == provider_id))
        provider = result.scalar_one_or_none()
        if provider and not provider.deleted:
            await collect_usage(provider, db)
