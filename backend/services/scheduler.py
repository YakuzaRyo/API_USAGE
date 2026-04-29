import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
logger = logging.getLogger("backend.services.scheduler")

_jobs: dict[int, str] = {}  # provider_id -> job_id


def init_scheduler():
    if not scheduler.running:
        scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)


def register_job(provider_id: int, interval_seconds: int, func):
    if provider_id in _jobs:
        remove_job(provider_id)
    job = scheduler.add_job(
        func,
        trigger="interval",
        seconds=interval_seconds,
        args=[provider_id],
        id=f"provider_{provider_id}",
        replace_existing=True,
    )
    _jobs[provider_id] = job.id
    logger.info("Job registered | provider_id=%s interval=%s", provider_id, interval_seconds)


def remove_job(provider_id: int):
    job_id = _jobs.pop(provider_id, None)
    if job_id and scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    logger.info("Job removed | provider_id=%s", provider_id)


def reschedule_job(provider_id: int, new_interval: int, func):
    remove_job(provider_id)
    if new_interval > 0:
        register_job(provider_id, new_interval, func)
    logger.info("Job rescheduled | provider_id=%s new_interval=%s", provider_id, new_interval)
