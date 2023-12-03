from collections.abc import Iterable

import dateparser
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class InsiderMediaNetSpider(scrapy.Spider):
    name = "insider-media.net"
    allowed_domains = ["insider-media.net"]

    base_url = "https://insider-media.net"
    next_page_url_pattern = f"{base_url}/news?page={{page}}"

    total_pages = 550

    custom_settings = {
        "PROXY_ENABLE": True,
        "DOWNLOAD_HANDLERS": {
            "http": "news.middlewares.proxy.handlers.RotatingProxiesDownloadHandler",
            "https": "news.middlewares.proxy.handlers.RotatingProxiesDownloadHandler",
        },
    }

    def start_requests(self) -> Iterable[Request]:
        for page in range(1, self.total_pages + 1):
            url = self.next_page_url_pattern.format(page=page)
            yield Request(url=url, callback=self.parse_news_list)

    def parse_news_list(self, response: HtmlResponse) -> Iterable[Request]:
        news_list = response.xpath('//div[@class="news-image"]/a/@href')
        for url in news_list.getall():
            yield response.request.replace(url=url, callback=self.parse_news)

    def parse_news(self, response: HtmlResponse) -> dict:
        title = response.css(".page-title-content h1::text").get()
        texts = response.xpath('//div[@class="article-content"]//p/text()').getall()
        date = response.css(".sub-bread::text").getall()
        return {
            "url": response.url,
            "title": title,
            "text": self._process_text(values=texts),
            "date": self._process_date(value=date),
        }

    @staticmethod
    def _process_text(values: list[str]) -> str:
        return "".join(values).strip().replace("\n", "")

    @staticmethod
    def _process_date(value: str) -> str:
        raw_date = value[1].strip()
        return dateparser.parse(date_string=raw_date).isoformat()
