BOT_NAME = "news"

SPIDER_MODULES = ["news.spiders"]
NEWSPIDER_MODULE = "news.spiders"


PROXY_ENABLE = False
PROXIES_LIST = ["<put-ip-addresses-here>"]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/85.0.4183.102 Safari/537.36"
)

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    ),
    "Accept-Language": "en",
    "From": "googlebot(at)googlebot.com",
    "Connection": "keep-alive",
}

DOWNLOADER_MIDDLEWARES = {
    "news.middlewares.proxy.random_proxy.RandomProxyMiddleware": 550
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
