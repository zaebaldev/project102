import logging
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from app.db.db_helper import db_helper
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.worker import broker

log = logging.getLogger(__name__)


# runs every minute, if you want to run it every 2 days, change to "0 0 */2 * *"
@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def delete_unverified_users(
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
) -> None:
    log.info("Starting deletion of unverified users")
    repo = UserRepository(session=session, model=User)
    service = UserService(session=session, repo=repo)
    row_count = await service.delete_unverified_users(
        expiration_delta=2 * 24 * 60 * 60
    )  # 2 days
    log.info("Deleted %s unverified users", row_count)
