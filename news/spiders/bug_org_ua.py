from collections.abc import Iterable

import dateparser
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class BugOrgUaSpider(scrapy.Spider):
    name = "bug.org.ua"
    allowed_domains = ["bug.org.ua"]

    next_page_url_pattern = "https://bug.org.ua/news/page/{page}/"

    total_pages = 1200

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
        news_list = response.xpath('//div[@class="newsblock__item__title"]/a/@href')
        for url in news_list.getall():
            yield response.request.replace(url=url, callback=self.parse_news)

    def parse_news(self, response: HtmlResponse) -> dict:
        title = response.css(".news_item__title h1::text").get()
        texts = response.css(".news_item__content p::text").getall()
        date = response.xpath('//div[@class="news_item__date"]//text()').getall()
        return {
            "url": response.url,
            "title": title,
            "text": self._process_text(values=texts),
            "date": self._process_date(values=date),
        }

    @staticmethod
    def _process_text(values: list[str]):
        return "".join(values).strip().replace("\n", "")

    @staticmethod
    def _process_date(values: list[str]) -> str:
        raw_value = "".join(values).strip().replace("\n", "")
        date_value = values[2] if "Цей запис" in raw_value else values[0]
        parsed_date = dateparser.parse(
            date_string=date_value, date_formats=["%d.%m.%Y"]
        )
        return parsed_date.isoformat()
