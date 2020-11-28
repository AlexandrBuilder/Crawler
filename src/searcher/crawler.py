import asyncio
from typing import Optional

from searcher.clients.request_client import RequestClient
from searcher.core.logger import Logger
from searcher.helpers.url_helper import UrlHelper
from searcher.services.page_service import PageHandlerService
from searcher.routes_collection import RouteCollection
from searcher.settings import Settings


class Crawler:

    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.logger = logger

        self.root_url = settings.root_url
        self.max_depth = settings.max_depth
        self.max_request_count = settings.max_request_count

        self.route_collection = RouteCollection(self.max_depth)

    async def start_workers_async(self) -> None:
        self.route_collection.add_route(self.root_url, 0)
        await self.send_request_collection_async()

    async def send_request_collection_async(self) -> None:
        while True:
            if self.route_collection.have_routes():
                tasks = []
                for route in self.route_collection.get_route_collection_by_count(self.max_request_count):
                    tasks.append(self.send_request_async(**route))

                await asyncio.gather(*tasks)
            else:
                break

    async def send_request_async(
            self,
            url: str,
            depth: int,
            parent_url_id: Optional[int] = None,
            link_text: Optional[str] = None
    ) -> None:
        is_success = False
        content = None

        try:
            is_success, content = await RequestClient.get_request_text_async(url)
            self.logger.info(f'Send by url: {url}')
        except Exception as ex:
            self.logger.error(f'Error by url: {url}. Error: {ex}')

        self.route_collection.remove_route(url)

        if is_success:
            await self.handler_request(url, depth, content, parent_url_id, link_text)

    async def handler_request(
            self,
            url: str,
            depth: int,
            content: str,
            parent_url_id: Optional[int] = None,
            link_text: Optional[str] = None
    ) -> None:
        page_handler = PageHandlerService(url, content, parent_url_id, link_text)
        await page_handler.save_index_by_content()
        url_id = await page_handler.get_url_id()

        depth += 1
        host = UrlHelper.get_host_by_url(url)

        for url_child, link_text in page_handler.get_new_urls():
            self.route_collection.add_route(url_child, depth, host, url_id, link_text)
