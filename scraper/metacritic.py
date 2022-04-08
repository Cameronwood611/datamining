from lxml import html
from lxml.html import HtmlElement

from utils import sxpath


def get_review_alternate(category: str, html: HtmlElement) -> dict:
    review = dict()
    overall_score = sxpath(html, ".//div[contains(@class, 'c-siteReviewScore')]/span/text()")
    review[f"{category}_overall_score"] = overall_score[0]

    reviews = sxpath(html, ".//div[@class='c-EntertainmentProductScoreGraph g-outer-spacing-top-large u-flexbox']")
    review_types = ["positive", "mixed", "negative"]
    for i, review_html in enumerate(reviews):
        review_type = review_types[i]
        review_score = sxpath(review_html, ".//span/text()")[0]
        review_type = f"{category}_{review_type}_score"
        review[review_type] = review_score
    return review


def get_review(category: str, html: HtmlElement) -> dict:
    review = dict()
    overall_score = sxpath(html, ".//a[@class='metascore_anchor']/div/text()")
    review[f"{category}_overall_score"] = overall_score[0]

    reviews = sxpath(html, ".//*[@class='chart_wrapper']")
    for review_html in reviews:
        review_type = sxpath(review_html, ".//div[@class='label fl']/text()")[0].strip(":")
        review_score = sxpath(review_html, ".//div[@class='count fr']/text()")[0]
        review_type = f"{category}_{review_type}_score".lower()
        review[review_type] = review_score
    return review


def get_meta_reviews(raw_html: str) -> dict:
    context = html.fromstring(raw_html)
    reviews = sxpath(context, ".//body//div[@id='nav_to_metascore']//div[@class='distribution']")
    if not reviews:
        reviews = sxpath(context, ".//body//div[@class='c-entertainmentProductScoreInfo g-inner-spacing-bottom-xlarge u-clearfix']")
        critic_html, user_html = reviews
        critic_review = get_review_alternate("critic", critic_html)
        user_review = get_review_alternate("user", critic_html)
        return {**critic_review, **user_review}

    critic_html, user_html = reviews
    critic_review = get_review("critic", critic_html)
    user_review = get_review("user", user_html)

    return {**critic_review, **user_review}
