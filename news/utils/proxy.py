import base64
from urllib.parse import unquote, urlunparse
from urllib.request import _parse_proxy  # type: ignore

from scrapy import Request


def set_proxy(request: Request, url: str) -> None:
    """
    Set proxy ip to Request Meta and put Proxy Authorization to request headers

    :param request: scrapy Request object
    :param url: proxy url
    :return:
    """
    credentials, proxy_url = parse_proxy(url)
    request.meta["proxy"] = proxy_url

    if credentials:
        request.headers["Proxy-Authorization"] = "Basic " + credentials.decode("utf-8")


def set_proxy_for_url(url: str) -> tuple[dict, str]:
    """
    Parse proxy url and set Proxy Authorization to headers dict

    :param url: proxy url
    :return: dict with Proxy Authorization header and raw proxy ip
    """
    credentials, proxy_url = parse_proxy(url)
    headers = {}

    if credentials:
        headers["Proxy-Authorization"] = "Basic " + credentials.decode("utf-8")

    return headers, proxy_url


def parse_proxy(url: str, _type: str = "http") -> tuple[bytes | None, str]:
    """
    Proxy url parser.

    :param url: proxy url
    :param _type: url schema type
    :return: proxy credentials and proxy ip address
    """
    proxy_type, user, password, host_port = _parse_proxy(url)
    proxy_url = urlunparse((proxy_type or _type, host_port, "", "", "", ""))

    credentials: bytes | None = None

    if user and password:
        user_password = f"{unquote(user)}:{unquote(password)}"
        credentials = base64.b64encode(user_password.encode("utf-8")).strip()

    return credentials, proxy_url
