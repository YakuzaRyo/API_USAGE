import asyncio
import sqlalchemy as sa

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select

from alembic.config import Config as AlembicConfig
from alembic import command

from logging_config import setup_logging
from database import engine, init_db, AsyncSessionLocal
from models import Provider
from routers import providers, stats, categories
from services.scheduler import init_scheduler, shutdown_scheduler, register_job


def _run_migrations():
    """Run Alembic with a dedicated sync engine, disposed immediately after."""
    import logging
    logger = logging.getLogger("backend.migrations")
    sync_url = "sqlite:///./data/app.db"
    sync_engine = sa.create_engine(sync_url)
    alembic_cfg = AlembicConfig("alembic.ini")
    try:
        from alembic.script import ScriptDirectory
        from alembic.runtime.migration import MigrationContext
        with sync_engine.connect() as conn:
            ctx = MigrationContext.configure(conn)
            current = ctx.get_current_revision()
            script = ScriptDirectory.from_config(alembic_cfg)
            head = script.get_current_head()
            if current == head:
                logger.info("Migrations already at head (%s), skipped", head)
                return
        logger.info("Running migrations from %s to %s", current or "base", head)
        command.upgrade(alembic_cfg, "head")
    finally:
        sync_engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    # 1. Migrations first (before any async engine connects)
    await asyncio.to_thread(_run_migrations)

    # 2. Init async DB (creates tables if fresh)
    await init_db()

    # 3. Start scheduler
    init_scheduler()
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Provider).where(Provider.deleted == False, Provider.interval_seconds > 0)
        )
        for p in result.scalars().all():
            register_job(p.id, p.interval_seconds, providers._scheduled_collect)

    yield

    shutdown_scheduler()
    await engine.dispose()


app = FastAPI(title="LLM Usage Monitor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(providers.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])


@app.get("/")
async def root():
    return {"message": "LLM Usage Monitor API"}
