import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np


def get_url(url: str, header: dict) -> requests:
    """
    Function which gets response from provided url and header.
    :param url: URL of desired webpage.
    :param header: header containing ID of person scraping and web-browser info.
    :return: response of the page.
    if there is an error retrieving response error message is shown.
    """
    response = requests.get(url, headers=header)

    if not response.ok:
        print(f"There is an {response} error")
    else:
        return response


def make_beautiful_soup(response: requests) -> BeautifulSoup:
    """
    Function which creates beautiful soup from the response.

    :param response: Response created after using request library (get_url function).
    :return: BeautifulSoup element.
    """
    return BeautifulSoup(response.text, 'html.parser')


def collect_movie_categories(url: str, header: dict) -> list:
    """
    Function which collects movie categories (main genres) from IMDB webpage.

    :param url: URL to IMDB webpage sorted by category.
    :param header: header containing ID of person scraping and web-browser info.
    :return: A list with collected movie categories.
    """
    response = get_url(url=url, header=header)
    soup = make_beautiful_soup(response)

    all_categories = soup.find_all('div', class_="widget_image")

    return [movie_genre.find('img')['title'] for movie_genre in all_categories]


def create_page_list(number_of_items_to_scrape: int, list_to_store_results: list) -> list:
    """
    Function which takes the number of desired movies to scrape and create a list with movie ID, required to iterate
     through the pages.

    :param number_of_items_to_scrape: The desired number of movies to scrape.
    :param list_to_store_results: a list to store converted results.
    :return: A list with movie ID with which required pages start.
    """
    for item in range(1, number_of_items_to_scrape + 1, 50):
        list_to_store_results.append(item)
    return list_to_store_results


def scrape_one_page(category: str, page: int, timeout: float, header: dict) -> BeautifulSoup:
    """
    Function which collect all list information containing information about the movie from a desired page.

    :param category: category of the movie directory.
    :param page: the first movie ID on the page required to scrape.
    :param timeout: Time duration between requests not to spam the server.
    :param header: header containing ID of person scraping and web-browser info.
    :return: BeautifulSoup object, containing all movie information from the page.
    """
    time.sleep(timeout)
    print(f'Now scraping {category} movies from page starting with movie id {page}')

    url = f'https://www.imdb.com/search/title/?genres={category}&sort=boxoffice_gross_us,desc&start={page}&explore=title_type,genres&ref_=adv_nxt'
    page_response = get_url(url=url, header=header)
    soup = make_beautiful_soup(page_response)

    all_movies_on_page = soup.find_all('div', class_="lister-item")

    return all_movies_on_page


def get_movie_title(movie_info: BeautifulSoup, list_to_collect_titles: list) -> str:
    """
    Function which gathers movie title from the provided BeautifulSoup object.

    :param movie_info: BeautifulSoup object containing movie info.
    :param list_to_collect_titles: a list where to store collected movie title.
    :return: appends the title to the selected list. If not provided None is returned.
    """

    try:
        title = movie_info.find('span', class_='lister-item-index').find_next().text
        return list_to_collect_titles.append(title)
    except:
        return list_to_collect_titles.append(np.nan)


def get_movie_year(movie_info: BeautifulSoup, list_to_collect_movie_year: list) -> str:
    """
    Function which gathers movie release year from the provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing movie info.
    :param list_to_collect_movie_year: a list where to store collected movie release year.
    :return: appends the movie release year to selected list. If not provided None is returned.
    """
    try:
        year = movie_info.find('span', class_="lister-item-year").text[1:5]
        return list_to_collect_movie_year.append(year)
    except:
        return list_to_collect_movie_year.append(np.nan)


def get_movie_certificate(movie_info: BeautifulSoup, list_to_store_certificate: list) -> str:
    """
    Function which gathers movie certificate(age restrictions) from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_certificate: a list where to store collected movie certificates
    :return: appends the movie certificate to selected list. If not provided None is returned.
    """
    try:
        certificate = movie_info.find('span', class_="certificate").text
        return list_to_store_certificate.append(certificate)
    except:
        return list_to_store_certificate.append(np.nan)


def get_movie_runtime(movie_info: BeautifulSoup, list_to_store_runtime: list) -> str:
    """
    Function which gathers runtime of the movie from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie
    :param list_to_store_runtime: a list where to store collected movie runtime.
    :return: appends the runtime of the movie to selected list. If not provided None is returned.
    """
    try:
        runtime = movie_info.find('span', class_="runtime").text
        return list_to_store_runtime.append(runtime)
    except:
        return list_to_store_runtime.append(np.nan)


def get_movie_genres(movie_info: BeautifulSoup, list_to_store_genres: list) -> str:
    """
    Function which gathers associated movie genres from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_genres: a list to store collected movie genres.
    :return: appends the associated movie genres to the selected list. If not provided None is returned.
    """
    try:
        movie_genres = movie_info.find('span', class_="genre").text.rstrip()[1:]
        return list_to_store_genres.append(movie_genres)
    except:
        return list_to_store_genres.append(np.nan)


def get_movie_rating(movie_info: BeautifulSoup, list_to_store_rating: list) -> str:
    """
    Function which gathers movie IMDB rating from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_rating: a list to store collected movie rating.
    :return: appends the IMDB rating to the selected list. If not provided None is returned.
    """
    try:
        rating = movie_info.find('div', class_="inline-block ratings-imdb-rating")['data-value']
        return list_to_store_rating.append(rating)
    except:
        return list_to_store_rating.append(np.nan)


def get_movie_metascore(movie_info: BeautifulSoup, list_to_store_metascore: list) -> str:
    """
    Function which gathers movie Metascore rating from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_metascore: a list to store collected Metascore rating.
    :return: appends Metascore rating to the selected list. If not provided None is returned.
    """
    try:
        metascore = movie_info.find('span', class_="metascore").text.rstrip()
        return list_to_store_metascore.append(metascore)
    except:
        return list_to_store_metascore.append(np.nan)


def get_movie_votes(movie_info: BeautifulSoup, list_to_store_votes: list) -> str:
    """
    Function which gathers the number of votes from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_votes: a list to store collected number of votes.
    :return: appends the number of votes to the selected list. If not provided None is returned.
    """
    try:
        total_votes = movie_info.find('p', class_="sort-num_votes-visible").findChildren('span')[1]['data-value']
        return list_to_store_votes.append(total_votes)
    except:
        return list_to_store_votes.append(np.nan)


def get_movie_box_office(movie_info: BeautifulSoup, list_to_store_box_office: list) -> str:
    """
    Function which gathers US box office earnings from provided BeautifulSoup info.

    :param movie_info: BeautifulSoup object containing info about the movie.
    :param list_to_store_box_office: a list to store collected number of votes.
    :return: appends the US box office earnings to the selected list. If not provided None is returned.

    """
    try:
        box_office = movie_info.find('p', class_="sort-num_votes-visible").findChildren('span')[4]['data-value'].replace(',', '')
        return list_to_store_box_office.append(box_office)
    except:
        return list_to_store_box_office.append(np.nan)


def get_movie_category(category: str, list_to_store_categories: list) -> str:
    """
    Function which takes the movie category and appends it to the list.

    :param category: category of the movie.
    :param list_to_store_categories: a list to store collected category names for movie.
    :return: appends the category name to the selected list.
    """
    try:
        return list_to_store_categories.append(category)
    except:
        return list_to_store_categories.append(np.nan)


def create_dataframe_from_dictionary(dictionary: dict) -> pd.DataFrame:
    """
    Crates a data frame from provided dictionary.

    :param dictionary: dictionary containing all information about the movies.
    :return: pandas DataFrame.
    """
    # To avoid errors:
    # If scraped results are in unequal lengths replaces missing values with None.
    dataframe = pd.DataFrame.from_dict(dictionary, orient='index')
    dataframe = dataframe.transpose()

    print(" >> Scrapping finished successfully << ")
    return dataframe


def write_to_csv(dataframe, title_of_csv_file: str):
    """
    Creates a csv file.

    :param dataframe: Pandas dataframe which should be used to create csv
    :param title_of_csv_file: desired csv file name
    :return: returns csv file
    """

    print(" >> Your csv file was created successfully << ")
    return dataframe.to_csv(f'{title_of_csv_file}.csv', index=None, header=True, na_rep='None')


def create_dictionary_for_movies(title: list,
                                 release_year: list,
                                 certificate: list,
                                 runtime: list,
                                 genres: list,
                                 category: list,
                                 rating: list,
                                 metascore: list,
                                 votes: list,
                                 box_office: list) -> dict:
    """
    Creates dictionary from the gathered movie information.

    :param title: list of titles of the movies.
    :param release_year: list of release years of the movies.
    :param certificate: list of certificates of the movies.
    :param runtime: list of runtimes of the movies.
    :param genres:  list of  genres of the movies.
    :param category: list of categories of the movies.
    :param rating: list of movie IMDB ratings.
    :param metascore: list of movie Metascore Ratings
    :param votes:  list of votes of the movies.
    :param box_office: list of US box office earnings.
    :return: dictionary containing all provided information.
    """
    dictionary_containing_all_scrapped_info = {

        "title": title,
        "year": release_year,
        "certificate": certificate,
        "length": runtime,
        "genres": genres,
        "category": category,
        "rating": rating,
        "metascore": metascore,
        "total_votes": votes,
        "US_box_office": box_office
    }

    return dictionary_containing_all_scrapped_info


def collect_information(number_of_items: int, main_category_list: list, timeout: float, header: dict) -> pd.DataFrame:
    """
    Function which scrapes IMDB web page.

    :param number_of_items: Number of movies per category to scrape.
    :param main_category_list: a list with category names.
    :param timeout: Time duration between requests not to spam the server.
    :param header: header containing ID of person scraping and web-browser info.
    :return: pandas dataframe containing scraped data.
    """
    title_list, page_list, year_list, certificate_list, runtime_list, \
    movie_genre_list, rating_list, metascore_list, total_votes_list, US_box_office_list, \
    category_list = ([] for i in range(11))

    create_page_list(number_of_items_to_scrape=number_of_items,
                     list_to_store_results=page_list)

    for genre in main_category_list:

        for page in page_list:

            all_movies_on_page = scrape_one_page(category=genre,
                                                 page=page,
                                                 timeout=timeout,
                                                 header=header)

            for movie in all_movies_on_page:
                get_movie_title(movie_info=movie, list_to_collect_titles=title_list)
                get_movie_year(movie_info=movie, list_to_collect_movie_year=year_list)
                get_movie_certificate(movie_info=movie, list_to_store_certificate=certificate_list)
                get_movie_runtime(movie_info=movie, list_to_store_runtime=runtime_list)
                get_movie_genres(movie_info=movie, list_to_store_genres=movie_genre_list)
                get_movie_rating(movie_info=movie, list_to_store_rating=rating_list)
                get_movie_metascore(movie_info=movie, list_to_store_metascore=metascore_list)
                get_movie_votes(movie_info=movie, list_to_store_votes=total_votes_list)
                get_movie_category(category=genre, list_to_store_categories=category_list)
                get_movie_box_office(movie_info=movie, list_to_store_box_office=US_box_office_list)

    scraped_info = create_dictionary_for_movies(title=title_list,
                                                release_year=year_list,
                                                certificate=certificate_list,
                                                runtime=runtime_list,
                                                genres=movie_genre_list,
                                                category=category_list,
                                                rating=rating_list,
                                                metascore=metascore_list,
                                                votes=total_votes_list,
                                                box_office=US_box_office_list)

    return create_dataframe_from_dictionary(scraped_info)
