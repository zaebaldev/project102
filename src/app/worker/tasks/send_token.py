import asyncio
import logging

from app.worker.taskiq_broker import broker

log = logging.getLogger(__name__)


@broker.task
async def send_verification_token(
    email: str,
    token: str,
) -> dict:
    try:
        log.info("Send verification token %s to %s", token, email)
        await asyncio.sleep(5)  # TODO: send token to email
        log.info("Verification token %s to %s sent successfully", token, email)
        return {
            "status": "success",
            "result": "Verification token sent",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
