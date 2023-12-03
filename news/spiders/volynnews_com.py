from collections.abc import Iterable

import dateparser
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse


class VolynnewsComSpider(scrapy.Spider):
    name = "volynnews.com"
    allowed_domains = ["volynnews.com"]

    base_url = "https://www.volynnews.com"
    next_page_url_pattern = f"{base_url}/news/all/?page={{page}}"

    total_pages = 2120

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
        news_list = response.xpath('//h4[@class="media-heading"]/a/@href')
        for path in news_list.getall():
            yield response.request.replace(
                url=self.base_url + path, callback=self.parse_news
            )

    def parse_news(self, response: HtmlResponse) -> dict:
        title = response.css(".title_news_video h1::text").get()
        texts = response.css(".text_video_news2::text").getall()
        date = response.css(".date_news_block1::text").get()
        return {
            "url": response.url,
            "title": title,
            "text": self._process_text(values=texts),
            "date": self._process_date(value=date),
        }

    @staticmethod
    def _process_text(values: list[str]):
        return "".join(values).strip().replace("\n", "")

    @staticmethod
    def _process_date(value: str) -> str:
        return dateparser.parse(date_string=value).isoformat()
