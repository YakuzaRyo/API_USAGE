import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from models import Provider, UsageRecord, CollectionLog
from services.crypto import decrypt

logger = logging.getLogger("backend.services.collector")


def extract_value(data: dict, path: str):
    """Extract a value from nested dict/list using dot-notation path."""
    parts = path.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (IndexError, ValueError):
                return None
        else:
            return None
    return current


async def _call_api(url: str, api_key: str) -> tuple[int, dict | str]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, headers={"Authorization": f"Bearer {api_key}"})
            if resp.status_code >= 400:
                return resp.status_code, resp.text[:500]
            return resp.status_code, resp.json()
    except Exception as e:
        return -1, str(e)


async def collect_usage(provider: Provider, db: AsyncSession) -> tuple[dict, dict | None]:
    api_key = decrypt(provider.api_key)
    base = provider.base_url.rstrip("/")

    # ── 1. Usage ──────────────────────────
    usage_result = {}
    try:
        url = f"{base}{provider.usage_api_path}"
        status, data = await _call_api(url, api_key)
        if status < 0 or status >= 400:
            logger.error("Usage API error | provider_id=%s status=%s error=%s", provider.id, status, data)
            db.add(CollectionLog(provider_id=provider.id, status="error",
                error_message=f"Usage API error: {status} {data}"))
            usage_result = {"status": "error", "message": f"HTTP {status}" if status > 0 else str(data)}
        else:
            mapping = provider.usage_mapping or {}
            total_tokens = 0
            cost = 0.0
            if mapping.get("total_tokens"):
                total_tokens = extract_value(data, mapping["total_tokens"]) or 0
            if mapping.get("cost"):
                cost = extract_value(data, mapping["cost"]) or 0.0

            models = provider.models or ["default"]
            record_count = 0
            for model in models:
                db.add(UsageRecord(
                    provider_id=provider.id, model=model,
                    tokens_used=int(total_tokens) // len(models),
                    cost=float(cost) / len(models),
                ))
                record_count += 1
            db.add(CollectionLog(provider_id=provider.id, status="ok", record_count=record_count))
            usage_result = {"status": "ok", "record_count": record_count,
                           "total_tokens": int(total_tokens), "cost": float(cost)}
            logger.info("Usage collection succeeded | provider_id=%s record_count=%s tokens=%s cost=%s",
                         provider.id, record_count, int(total_tokens), float(cost))
    except Exception as e:
        logger.error(f"Usage collection error for provider {provider.id}: {e}")
        db.add(CollectionLog(provider_id=provider.id, status="error",
            error_message=f"Usage collection exception: {e}"))
        usage_result = {"status": "error", "message": str(e)}

    # ── 2. Balance ────────────────────────
    balance_result = None
    if provider.balance_api_path:
        try:
            url = f"{base}{provider.balance_api_path}"
            status, data = await _call_api(url, api_key)
            if status < 0 or status >= 400:
                db.add(CollectionLog(provider_id=provider.id, status="error",
                    error_message=f"Balance API error: {status} {data}"))
                balance_result = {"status": "error", "message": f"HTTP {status}" if status > 0 else str(data)}
            else:
                mapping = provider.balance_mapping or {}
                balance = None
                if mapping.get("balance"):
                    balance = extract_value(data, mapping["balance"])
                if balance is not None:
                    provider.last_balance = float(balance)
                db.add(CollectionLog(provider_id=provider.id, status="ok", record_count=1,
                                     balance=float(balance) if balance is not None else None))
                balance_result = {"status": "ok", "balance": float(balance) if balance is not None else None}
                logger.info("Balance collection succeeded | provider_id=%s balance=%s",
                             provider.id, balance if balance is not None else "N/A")
        except Exception as e:
            logger.error(f"Balance collection error for provider {provider.id}: {e}")
            db.add(CollectionLog(provider_id=provider.id, status="error",
                error_message=f"Balance collection exception: {e}"))
            balance_result = {"status": "error", "message": str(e)}

    await db.commit()
    return usage_result, balance_result
