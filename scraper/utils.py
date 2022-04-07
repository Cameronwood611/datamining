
import csv
import json
import socket

import aiohttp
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
from lxml.html import HtmlElement


def write_to_json(data: dict, path: str):
    with open(path, 'w') as f:
        json.dump(data, f)


def write_to_csv(fields: list, rows: list, path: str):
    with open(path, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)

def sxpath(context: HtmlElement, xpath: str) -> list:
    res = context.xpath(xpath, smart_strings=False)
    return res


def use_bs4(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


async def new_session() -> aiohttp.ClientSession:
    user_agent = get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    return aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False), headers=headers
    )

