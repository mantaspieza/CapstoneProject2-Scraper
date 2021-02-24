from Scraper.IMDB_scrapper import Scraper
from bs4 import BeautifulSoup
import pandas as pd


with open(
    "test_data/test_movie_data.html"
) as v:
    list_of_movies = BeautifulSoup(v.read(), "html.parser")


scraper = Scraper()


def test_get_movie_title():
    title = []
    result = scraper.get_movie_title(
        movie_info=list_of_movies, list_to_collect_titles=title
    )
    assert result == ["Incredibles 2"]


def test_get_movie_year():
    year = []
    scraper.get_movie_year(list_of_movies, year)
    assert year == [2018]


def test_get_movie_certificate():
    movie_certificate = []
    scraper.get_movie_certificate(list_of_movies, movie_certificate)
    assert movie_certificate == ["PG"]


def test_get_movie_runtime():
    movie_runtime = []
    scraper.get_movie_runtime(list_of_movies, movie_runtime)
    assert movie_runtime == ["118 min"]


def test_get_movie_genres():
    movie_genres = []
    scraper.get_movie_genres(list_of_movies, movie_genres)
    assert movie_genres == ["Animation, Action, Adventure"]


def test_get_movie_rating():
    movie_rating = []
    scraper.get_movie_rating(list_of_movies, movie_rating)
    assert movie_rating == [7.6]


def test_get_movie_metascore():
    movie_metascore = []
    scraper.get_movie_metascore(list_of_movies, movie_metascore)
    assert movie_metascore == [80]


def test_get_movie_votes():
    movie_votes = []
    scraper.get_movie_votes(list_of_movies, movie_votes)
    assert movie_votes == [251410]


def test_get_movie_box_office():
    movie_box_office = []
    scraper.get_movie_box_office(list_of_movies, movie_box_office)
    assert movie_box_office == [608581744]


def test_create_dataframe_from_dictionary():
    dictionary = {"title": "title of the movie", "runtime": 80}
    result = scraper.create_dataframe_from_dictionary(dictionary)
    assert type(result) == pd.DataFrame


def test_create_dictionary_for_movies():
    test_title = ["a", "b", "c"]
    test_rating = ["a", "b", "c"]
    test_year = ["a", "b", "c"]
    test_certificate = ["a", "b", "c"]
    test_genres = ["a", "b", "c"]
    test_runtime = ["a", "b", "c"]
    test_metascore = ["a", "b", "c"]
    test_votes = ["a", "b", "c"]
    test_box_office = ["a", "b", "c"]
    test_category = ["a", "b", "c"]

    dictionary = Scraper.create_dictionary_for_movies(
        title=test_title,
        rating=test_rating,
        release_year=test_year,
        certificate=test_certificate,
        genres=test_genres,
        runtime=test_runtime,
        metascore=test_metascore,
        votes=test_votes,
        box_office=test_box_office,
        category=test_category,
    )
    assert type(dictionary) == dict
