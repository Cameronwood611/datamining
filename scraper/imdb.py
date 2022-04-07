
import asyncio
from urllib.parse import urljoin

import requests
from lxml import html

from metacritic import get_meta_reviews
from utils import new_session, sxpath, use_bs4, write_to_csv, write_to_json


async def get_url_content(url: str) -> str:
    """ Get the raw html of a url response"""
    session = await new_session()
    response = await session.get(url)
    html = await response.text()
    await session.close()
    return html
    

async def extrapolate_metascore(url: str) -> dict:
    """ Extend review data of a movie from the metascore section """
    raw_html = await get_url_content(url)
    context = html.fromstring(raw_html)
    metacritic_url = sxpath(context, ".//body//div[@id='main']//div[@class='see-more']/a/@href")[0]
    meta_html = await get_url_content(metacritic_url)
    extra_reviews = get_meta_reviews(meta_html)
    return extra_reviews


async def traverse_imdb_movies(url):
    

    all_reviews = list()
    current_url = url
    while True:
        raw_html = await get_url_content(current_url)
        context = html.fromstring(raw_html)
        movies = sxpath(context, ".//body//h3[@class='lister-item-header']/a")
        for movie_node in movies:
            movie_title = movie_node.text_content()
            partial_movie_url = movie_node.get("href")
            full_movie_url = urljoin(url, partial_movie_url)
            print("COLLECTING MOVIE: ", movie_title)
            reviews = await get_movie_reviews(full_movie_url)
            movie_review = { "title": movie_title, "reviews": reviews }
            all_reviews.append(movie_review)
        partial_next_page_url = sxpath(context, ".//body//a[@class='lister-page-next next-page']/@href")
        if not partial_next_page_url:
            return {"reviews": all_reviews }
        print("Next page... \n")
        current_url = urljoin(url, partial_next_page_url[0])
            
    


async def get_movie_reviews(url: str) -> dict:
    html = await get_url_content(url)
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
            review_item = await extrapolate_metascore(metascore_url)

        results.append(review_item)

    result = dict()
    for d in results:
        result.update(d)
    return result


def json_to_csv(data: dict):
    expected_fields = ["user_review_count", "critic_review_count", "critic_overall_score", "critic_positive_score", 
    "critic_mixed_score", "critic_negative_score", "user_overall_score", "user_positive_score", "user_mixed_score", 
    "user_negative_score"]  # this expects the names to be consistent upon creation

    movies = data["reviews"]
    results = list()
    for movie in movies:
        row = [movie["title"]]
        for field in expected_fields:
            row.append(movie["reviews"].get(field))
        results.append(row)

    fields = ["title"] + expected_fields
    write_to_csv(fields, results, "test.csv")




def main():
    base_url = "https://www.imdb.com/search/title/?groups=oscar_winner&sort=release_date,asc"
    loop = asyncio.get_event_loop()
    reviews = loop.run_until_complete(traverse_imdb_movies(base_url))
    # reviews = loop.run_until_complete(get_movie_reviews("https://www.imdb.com/title/tt10366460/?ref_=adv_li_tt"))
    write_to_json(reviews, "test.json")
    json_to_csv(reviews)
    


main()
