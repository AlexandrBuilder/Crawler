from gino import GinoEngine, create_engine
from searcher.core.logger import Logger
from searcher.settings import Settings
from searcher.models import db


class PostgresConnectionManager:

    def __init__(self, setting: Settings, logger: Logger) -> None:
        self.postgres_dsn = setting.postgres_dsn
        self.logger = logger
        self._engine = None

    async def get_connection_async(self) -> GinoEngine:
        if not self._engine:
            self._engine = await create_engine(self.postgres_dsn)

        return self._engine

    async def create_connection_async(self) -> None:
        db.bind = await self.get_connection_async()
        self.logger.info(f'Database connected by "{self.postgres_dsn}"')

    async def close_connection_async(self) -> None:
        await self._engine.close()
