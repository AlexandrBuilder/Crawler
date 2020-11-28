from urllib.parse import urlparse


class UrlHelper:

    @staticmethod
    def get_host_by_url(url) -> str:
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme if parsed_url.scheme else 'https'
        return f'{scheme}://{parsed_url.netloc}/'
