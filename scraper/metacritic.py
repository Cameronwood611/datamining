from lxml import html
from lxml.html import HtmlElement

from utils import sxpath


def get_review(category: str, html: HtmlElement) -> dict:
    review = dict()
    overall_score = sxpath(html, ".//a[@class='metascore_anchor']/div/text()")[0]
    review[f"{category}_overall_score"] = overall_score

    reviews = sxpath(html, ".//*[@class='chart_wrapper']")
    for review_html in reviews:
        review_type = sxpath(review_html, ".//div[@class='label fl']/text()")[0].strip(":")
        review_score = sxpath(review_html, ".//div[@class='count fr']/text()")[0]
        review_type = f"{category}_{review_type}_score".lower()
        review[review_type] = review_score
    return review


def get_meta_reviews(raw_html: str) -> dict:
    context = html.fromstring(raw_html)
    critic_html, user_html = sxpath(context, ".//body//div[@id='nav_to_metascore']//div[@class='distribution']")
    critic_review = get_review("critic", critic_html)
    user_review = get_review("user", user_html)

    return {**critic_review, **user_review}
