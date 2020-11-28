from typing import Tuple
import http
import aiohttp


class RequestClient:

    @staticmethod
    async def get_request_text_async(url: str) -> Tuple[bool, str]:
        timeout = aiohttp.ClientTimeout(total=20)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                is_success = resp.status == http.HTTPStatus.OK
                content = await resp.text()
                return is_success, content
