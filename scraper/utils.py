
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
from lxml.html import HtmlElement


def sxpath(context: HtmlElement, xpath: str) -> list:
    res = context.xpath(xpath, smart_strings=False)
    return res


def use_bs4(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def create_headers():
    user_agent = get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    return headers
