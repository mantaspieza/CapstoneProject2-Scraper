from IMDB_scraper.IMDB_scrapper_class import Scraper
from bs4 import BeautifulSoup

with open(
        "/test_data/test_movie_data.html"
) as v:
    list_of_movies = BeautifulSoup(v.read(), "html.parser")


def test_get_movie_title():
    scraper = Scraper()
    title = scraper.get_movie_title(movie_info=list_of_movies)
    assert title == "Incredibles 2"


def test_get_movie_year():
    scraper = Scraper()
    movie_year = scraper.get_movie_year(movie_info=list_of_movies)
    assert movie_year == 2018


def test_get_movie_certificate():
    scraper = Scraper()
    certificate = scraper.get_movie_certificate(movie_info=list_of_movies)
    assert certificate == "PG"


def test_get_movie_runtime():
    scraper = Scraper()
    runtime = scraper.get_movie_runtime(movie_info=list_of_movies)
    assert runtime == '118 min'


def test_get_movie_genres():
    scraper = Scraper()
    genres = scraper.get_movie_genres(movie_info=list_of_movies)
    assert genres == "Animation, Action, Adventure"


def test_get_movie_rating():
    scraper = Scraper()
    rating = scraper.get_movie_rating(movie_info=list_of_movies)
    assert rating == 7.6


def test_get_movie_metascore():
    scraper = Scraper()
    metascore = scraper.get_movie_metascore(movie_info=list_of_movies)
    assert metascore == 80


def test_get_movie_votes():
    scraper = Scraper()
    votes = scraper.get_movie_votes(movie_info=list_of_movies)
    assert votes == 251410


def test_get_movie_box_office():
    scraper = Scraper()
    box_office = scraper.get_movie_box_office(movie_info=list_of_movies)
    assert box_office == 608581744

