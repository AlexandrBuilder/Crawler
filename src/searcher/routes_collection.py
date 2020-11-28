from typing import Optional, List
from urllib.parse import urlparse, urljoin


class RouteCollection:

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self._new_url_collection = {}
        self._finished_url_collection = []

    def add_route(
            self,
            url: str,
            depth: int,
            host: Optional[str] = None,
            parent_url_id: Optional[int] = None,
            link_text: Optional[str] = None
    ) -> None:
        if depth > self.max_depth:
            return

        parsed_uri = urlparse(url)
        if not parsed_uri.netloc or not parsed_uri.scheme:
            url = urljoin(host, url)

        self._new_url_collection[url] = {
            'url': url,
            'link_text': link_text,
            'depth': depth,
            'parent_url_id': parent_url_id
        }

    def remove_route(self, url: str) -> None:
        del self._new_url_collection[url]
        self._finished_url_collection.append(url)

    def have_routes(self) -> bool:
        return len(self._new_url_collection) > 0

    def get_route_collection_by_count(self, count: int) -> List[dict]:
        url_collection = list(self._new_url_collection.keys())[:count]
        return [self._new_url_collection[url] for url in url_collection]

    def is_not_know_route(self, url: str) -> bool:
        if url in self._new_url_collection or url in self._finished_url_collection:
            return True
        return False
