
import pandas as pd
from regex import F


def intersect_files():
    scraped_file = "../data/imdb.csv"
    kaggle_file = "../data/the_oscar_award.csv"
    output_file = "../data/oscars.csv"

    f1, f2 = pd.read_csv(scraped_file), pd.read_csv(kaggle_file)

    output = pd.merge(f1, f2, left_on="title", right_on="film")
    output.to_csv(output_file)


intersect_files()
