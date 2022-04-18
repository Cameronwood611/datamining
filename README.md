# Oscars Clustering and Prediction


## Background

Many of us have watched the Oscars but have you ever wondered if there was a way to predict which movies would win ahead of time? That's our goal and we have a few different ways to try and do this.

In order to make this happen, we must start with a fairly large dataset of all the Oscar nominees and winners so far. Not sure if you realize this, but it's a lot. Thankfully, we found a dataset on [kaggle](https://www.kaggle.com/datasets/unanimad/the-oscar-awar) that has some interesting attributes about each entry but not enough! Therefore, we had to manually scrape a bunch of data off [imdb](https://www.imdb.com/search/title/?groups=oscar_nominee&sort=release_date,asc).

Once we collected our data, we had to combined the two documents and clean them. Merging the documents was fairly straight forward but cleaning was tricky. There were many subtleties (having commas in large numbers, abbreviating 1000 as 1K, special characters not translating etc.) but after some time, we cleaned it up nicely.

With our clean dataset, we were able to move on to some really cool clustering and predictive algorithms.