import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import UsageRecord, Provider, CollectionLog

router = APIRouter()
logger = logging.getLogger("backend.routers.stats")


def _build_balance_query(provider_id: int | None = None):
    base = select(func.coalesce(func.sum(Provider.last_balance), 0.0))
    base = base.where(Provider.deleted == False)
    if provider_id:
        base = base.where(Provider.id == provider_id)
    return base


@router.get("/summary")
async def get_summary(
    provider_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Stats summary queried | provider_id=%s", provider_id or "all")
    base = select(
        func.coalesce(func.sum(UsageRecord.tokens_used), 0).label("total_tokens"),
        func.coalesce(func.sum(UsageRecord.cost), 0.0).label("total_cost"),
    )
    if provider_id:
        base = base.where(UsageRecord.provider_id == provider_id)

    result = await db.execute(base)
    row = result.one()

    # Active providers: count non-deleted providers
    prov_base = select(func.count(Provider.id)).where(Provider.deleted == False)
    if provider_id:
        prov_base = prov_base.where(Provider.id == provider_id)
    prov_result = await db.execute(prov_base)
    active_providers = prov_result.scalar() or 0

    bal_result = await db.execute(_build_balance_query(provider_id))
    total_balance = bal_result.scalar()

    # Balance consumed = initial total - current total
    first_balances_base = (
        select(func.coalesce(func.sum(CollectionLog.balance), 0.0))
        .where(
            CollectionLog.balance.isnot(None),
            CollectionLog.id.in_(
                select(func.min(CollectionLog.id))
                .where(CollectionLog.balance.isnot(None))
                .group_by(CollectionLog.provider_id)
            )
        )
    )
    if provider_id:
        first_balances_base = first_balances_base.where(CollectionLog.provider_id == provider_id)
    first_result = await db.execute(first_balances_base)
    initial_total = first_result.scalar() or 0.0
    balance_consumed = round(float(initial_total - total_balance), 4)

    symbol = "CNY"
    if provider_id:
        sym_result = await db.execute(select(Provider.currency_symbol).where(Provider.id == provider_id))
        s = sym_result.scalar_one_or_none()
        if s: symbol = s
    return {
        "total_tokens": int(row.total_tokens),
        "total_cost": round(float(row.total_cost), 4),
        "active_providers": int(active_providers),
        "total_balance": round(float(total_balance), 4),
        "balance_consumed": balance_consumed,
        "currency_symbol": symbol,
    }


@router.get("/trends")
async def get_trends(
    provider_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    date_col = func.date(UsageRecord.recorded_at).label("date")
    logger.info("Stats trends queried | provider_id=%s", provider_id or "all")
    base = select(
        date_col,
        func.sum(UsageRecord.tokens_used).label("tokens"),
        func.sum(UsageRecord.cost).label("cost"),
        func.sum(UsageRecord.balance).label("balance"),
    ).group_by(date_col).order_by(date_col)

    if provider_id:
        base = base.where(UsageRecord.provider_id == provider_id)

    result = await db.execute(base)
    rows = result.all()

    provider_name = None
    if provider_id:
        pres = await db.execute(select(Provider.name).where(Provider.id == provider_id))
        provider_name = pres.scalar_one_or_none()

    return [
        {
            "date": str(row.date),
            "tokens": int(row.tokens),
            "cost": round(float(row.cost), 4),
            "balance": round(float(row.balance or 0), 4),
            "provider_name": provider_name or "",
        }
        for row in rows
    ]


@router.get("/distribution")
async def get_distribution(
    provider_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    base = select(
        UsageRecord.model,
        func.sum(UsageRecord.tokens_used).label("tokens"),
    ).group_by(UsageRecord.model).order_by(func.sum(UsageRecord.tokens_used).desc())
    logger.info("Stats distribution queried | provider_id=%s", provider_id or "all")

    if provider_id:
        base = base.where(UsageRecord.provider_id == provider_id)

    result = await db.execute(base)
    rows = result.all()

    return [
        {"model": row.model, "tokens": int(row.tokens)}
        for row in rows
    ]


@router.get("/balance-history")
async def get_balance_history(
    provider_id: int | None = Query(None),
    days: int = Query(30, ge=1, le=365),
    start: str | None = Query(None),
    end: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Balance history queried | provider_id=%s days=%s", provider_id or "all", days)
    base = select(
        CollectionLog.created_at.label("date"),
        Provider.name.label("provider_name"),
        CollectionLog.balance,
        Provider.currency_symbol,
    ).join(Provider, CollectionLog.provider_id == Provider.id).where(
        CollectionLog.balance.isnot(None),
        Provider.deleted == False,
    )

    if start:
        base = base.where(CollectionLog.created_at >= datetime.fromisoformat(start))
    elif days:
        base = base.where(CollectionLog.created_at >= datetime.now(timezone.utc) - timedelta(days=days))
    if end:
        base = base.where(CollectionLog.created_at < datetime.fromisoformat(end) + timedelta(days=1))

    if provider_id:
        base = base.where(CollectionLog.provider_id == provider_id)

    base = base.order_by(CollectionLog.created_at.asc())

    result = await db.execute(base)
    return [
        {
            "date": row.date.isoformat(),
            "provider_name": row.provider_name,
            "balance": round(float(row.balance), 4),
            "currency_symbol": row.currency_symbol,
        }
        for row in result.all()
    ]


@router.get("/billing-summary")
async def get_billing_summary(
    provider_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Billing summary queried | provider_id=%s", provider_id or "all")
    prov_base = select(Provider).where(Provider.deleted == False)
    if provider_id:
        prov_base = prov_base.where(Provider.id == provider_id)
    prov_result = await db.execute(prov_base)
    providers = prov_result.scalars().all()

    items = []
    for p in providers:
        if p.billing_mode == "token_plan":
            amount = 0.0
            if p.monthly_fee and p.sub_start_date:
                start_date = datetime.fromisoformat(p.sub_start_date).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                months = max(0, (now.year - start_date.year) * 12 + (now.month - start_date.month))
                amount = round(float(p.monthly_fee) * months, 4)
            items.append({
                "provider_id": p.id, "provider_name": p.name,
                "billing_mode": p.billing_mode, "amount": amount,
                "currency_symbol": p.currency_symbol,
            })
        else:
            # API mode: balance_consumed
            first = await db.execute(
                select(func.coalesce(func.min(CollectionLog.balance), 0.0))
                .where(CollectionLog.provider_id == p.id, CollectionLog.balance.isnot(None))
            )
            initial = first.scalar() or 0.0
            consumed = round(float(initial - (p.last_balance or 0.0)), 4)
            items.append({
                "provider_id": p.id, "provider_name": p.name,
                "billing_mode": p.billing_mode, "amount": consumed,
                "currency_symbol": p.currency_symbol,
            })

    return items
