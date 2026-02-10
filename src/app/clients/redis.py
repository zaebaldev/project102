import logging

from redis.asyncio import ConnectionPool, Redis

from core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self, url) -> None:
        self.url = url
        self._pool: ConnectionPool | None = None
        self._client: Redis | None = None

    async def init(self) -> None:
        try:
            self._pool = ConnectionPool.from_url(self.url)
            self._client = Redis(connection_pool=self._pool)  # type: ignore
            await self._client.ping()  # type: ignore
            logger.info("Redis client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> Redis:
        if not self._client:
            raise RuntimeError(
                "Redis client is not initialized. Did you forget to call init()?"
            )
        return self._client


redis_client = RedisClient(str(settings.redis.url))
