import asyncio

from injector import Injector
from searcher.connection_managers.postgres_connection_manager import PostgresConnectionManager
from searcher.core.container import Container
from searcher.crawler import Crawler


class Application:

    def __init__(self) -> None:
        self.container = Injector(Container)

    async def start_tasks_async(self) -> None:
        postgres_connection_manager = self.container.get(PostgresConnectionManager)
        await asyncio.gather(postgres_connection_manager.create_connection_async())

    async def run(self) -> None:
        crawler = self.container.get(Crawler)
        await crawler.start_workers_async()

    async def stop_tasks_async(self) -> None:
        postgres_connection_manager = self.container.get(PostgresConnectionManager)
        await asyncio.gather(postgres_connection_manager.close_connection_async())
