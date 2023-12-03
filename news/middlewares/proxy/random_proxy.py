import logging
from collections.abc import Iterable
from itertools import cycle

from scrapy import Request
from scrapy.crawler import Crawler, Spider
from scrapy.exceptions import NotConfigured
from scrapy.settings import BaseSettings

from news.utils.proxy import set_proxy

logger = logging.getLogger(__name__)


class RandomProxyMiddleware:
    """
    For every request set proxy from ``PROXIES_LIST``.
    Works only if ``PROXY_ENABLE`` is True.
    """

    def __init__(self, proxies: list[str]) -> None:
        self._proxies = cycle(proxies)

    @property
    def proxy(self) -> Iterable[str]:
        """
        Pick next proxy from proxies list.
        """
        return next(self._proxies)

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "RandomProxyMiddleware":
        return cls.from_settings(crawler.settings)

    @classmethod
    def from_settings(cls, settings: BaseSettings) -> "RandomProxyMiddleware":
        if not settings.getbool("PROXY_ENABLE"):
            raise NotConfigured("Random Proxy is disabled in settings")

        if proxies := settings.getlist("PROXIES_LIST"):
            return cls(proxies=proxies)
        else:
            raise NotConfigured("Proxy list is empty")

    def process_request(self, request: Request, spider: Spider) -> None:
        """
        Process request and setup proxy.
        """
        if request.meta.get("_skip_proxy"):
            logger.info(f"Skip proxy for request to {request.url}")
            return None

        if request.meta.get("origin_proxy_url"):
            proxy = request.meta.get("origin_proxy_url")
        else:
            proxy = self.proxy

        logger.info(f"Request to {request.url}")
        logger.info(f"Proxy used: {proxy}")

        set_proxy(request=request, url=proxy)
