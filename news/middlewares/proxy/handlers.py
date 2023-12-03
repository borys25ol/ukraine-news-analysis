import warnings
from typing import Any

from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
from scrapy.core.downloader.tls import openssl_methods
from scrapy.crawler import Crawler
from scrapy.utils.misc import create_instance, load_object
from twisted.web.client import HTTPConnectionPool


class RotatingProxiesDownloadHandler(HTTPDownloadHandler):
    """
    Override `HTTPDownloadHandler` to not persistent connection pool.
    """

    def __init__(self, settings: Any, crawler: Crawler | None = None) -> None:
        super().__init__(settings)
        self._crawler = crawler

        from twisted.internet import reactor

        self._pool = HTTPConnectionPool(reactor, persistent=False)
        self._pool.maxPersistentPerHost = settings.getint(
            "CONCURRENT_REQUESTS_PER_DOMAIN"
        )
        self._pool._factory.noisy = False

        self._sslMethod = openssl_methods[settings.get("DOWNLOADER_CLIENT_TLS_METHOD")]
        self._contextFactoryClass = load_object(
            settings["DOWNLOADER_CLIENTCONTEXTFACTORY"]
        )
        # try method-aware context factory
        try:
            self._contextFactory = create_instance(
                objcls=self._contextFactoryClass,
                settings=settings,
                crawler=crawler,
                method=self._sslMethod,
            )
        except TypeError:
            # use context factory defaults
            self._contextFactory = create_instance(
                objcls=self._contextFactoryClass, settings=settings, crawler=crawler
            )
            msg = f"""
    '{settings["DOWNLOADER_CLIENTCONTEXTFACTORY"]}' does not accept `method` \
    argument (type OpenSSL.SSL method, e.g. OpenSSL.SSL.SSLv23_METHOD) and/or \
    `tls_verbose_logging` argument and/or `tls_ciphers` argument.\
    Please upgrade your context factory class to handle them or ignore them."""
            warnings.warn(msg)

        self._default_maxsize = settings.getint("DOWNLOAD_MAXSIZE")
        self._default_warnsize = settings.getint("DOWNLOAD_WARNSIZE")
        self._fail_on_dataloss = settings.getbool("DOWNLOAD_FAIL_ON_DATALOSS")
        self._disconnect_timeout = 1
