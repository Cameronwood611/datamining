
from urllib.parse import urljoin

import requests
from lxml import html

from metacritic import get_meta_reviews
from utils import create_headers, sxpath, use_bs4


def get_url_content(url: str) -> str:
    """ Get the raw html of a url response"""
    headers = create_headers()
    response = requests.get(url, headers=headers)
    html = response.text
    return html
    

def extrapolate_metascore(url: str) -> dict:
    """ Extend review data of a movie from the metascore section """
    raw_html = get_url_content(url)
    context = html.fromstring(raw_html)
    metacritic_url = sxpath(context, ".//body//div[@id='main']//div[@class='see-more']/a/@href")[0]
    meta_html = get_url_content(metacritic_url)
    extra_reviews = get_meta_reviews(meta_html)
    return extra_reviews


def get_imdb_data(url: str) -> list:
    html = get_url_content(url)
    soup = use_bs4(html)
    reviews = soup.findAll("a", {"class": "isReview"})

    results = list()
    for review in reviews:
        review_link = review["href"]  # links to each review (only metascore seems interesting)
        review_type = review.find(name="span", attrs={"class": "label"}).get_text()
        review_score = review.find(name="span", attrs={"class": "score"}).get_text()

        review_item = dict()
        if review_type == "User reviews":
            review_item = { "user_review_count": review_score }
        
        if review_type == "Critic reviews":
            review_item = { "critic_review_count": review_score }

        if review_type == "Metascore":
            metascore_url = urljoin(url, review_link)
            review_item = extrapolate_metascore(metascore_url)

        results.append(review_item)

    return results


reviews = get_imdb_data("https://www.imdb.com/title/tt10366460/?ref_=adv_li_tt")
print(reviews)
