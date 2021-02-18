import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np


class Scraper:

    def __init__(self):
        self.header = {'Turing-College-capstone-project-work': "Mozilla/5.0"}
        self.url_for_movie_categories = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"
        self.number_of_movies_per_category = 1
        self.title_of_csv_file = "scraped_imdb_file"
        self.timeout = 2

    def get_url(self, url: str, header: dict) -> requests:
        """

        :param url:
        :param header:
        :return:
        """

        self.response = requests.get(url, headers=header)

        if not self.response.ok:
            print(f"There is an {self.response} error")
        else:
            return self.response

    def make_beautiful_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.response.text, 'html.parser')

    def collect_movie_categories(self) -> list:
        """

        :return:
        """
        self.get_url(url=self.url_for_movie_categories, header=self.header)
        soup = self.make_beautiful_soup()

        all_categories = soup.find_all('div', class_="widget_image")

        return [movie_genre.find('img')['title'] for movie_genre in all_categories]

    def create_page_list(self) -> list:
        """

        :return:
        """
        page_list = []
        for item in range(1, self.number_of_movies_per_category + 1, 50):
            page_list.append(item)
        return page_list

    def scrape_one_page(self, category: str, page: int, timeout: float) -> BeautifulSoup:
        """

        :param category:
        :param page:
        :param timeout:
        :return:
        """
        time.sleep(timeout)
        print(f'Now scraping {category} movies from page starting with movie id {page}')

        url = f'https://www.imdb.com/search/title/?genres={category}&sort=boxoffice_gross_us,desc&start={page}&explore=title_type,genres&ref_=adv_nxt'
        self.get_url(url=url, header=self.header)
        soup = self.make_beautiful_soup()

        all_movies_on_page = soup.find_all('div', class_="lister-item")

        return all_movies_on_page

    @staticmethod
    def get_movie_title(movie_info: BeautifulSoup, list_to_collect_titles: list) -> str or None:
        """
        Function which gathers movie title from the provided BeautifulSoup object.

        :param movie_info: BeautifulSoup object containing movie info.
        :param list_to_collect_titles: a list where to store collected movie title.
        :return: appends the title to the selected list. If not provided None is returned.
        """

        try:
            title = movie_info.find('span', class_='lister-item-index').find_next().text
            return list_to_collect_titles.append(str(title))
        except:
            return list_to_collect_titles.append(np.nan)

    @staticmethod
    def get_movie_year(movie_info: BeautifulSoup, list_to_collect_movie_year: list) -> int or None:
        """
        Function which gathers movie release year from the provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing movie info.
        :param list_to_collect_movie_year: a list where to store collected movie release year.
        :return: appends the movie release year to selected list. If not provided None is returned.
        """
        try:
            year = movie_info.find('span', class_="lister-item-year").text[1:5]
            return list_to_collect_movie_year.append(int(year))
        except:
            return list_to_collect_movie_year.append(np.nan)

    @staticmethod
    def get_movie_certificate(movie_info: BeautifulSoup, list_to_store_certificate: list) -> str or None:
        """
        Function which gathers movie certificate(age restrictions) from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_certificate: a list where to store collected movie certificates
        :return: appends the movie certificate to selected list. If not provided None is returned.
        """
        try:
            certificate = movie_info.find('span', class_="certificate").text
            return list_to_store_certificate.append(str(certificate))
        except:
            return list_to_store_certificate.append(np.nan)

    @staticmethod
    def get_movie_runtime(movie_info: BeautifulSoup, list_to_store_runtime: list) -> str or None:
        """
        Function which gathers runtime of the movie from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie
        :param list_to_store_runtime: a list where to store collected movie runtime.
        :return: appends the runtime of the movie to selected list. If not provided None is returned.
        """
        try:
            runtime = movie_info.find('span', class_="runtime").text
            return list_to_store_runtime.append(str(runtime))
        except:
            return list_to_store_runtime.append(np.nan)

    @staticmethod
    def get_movie_genres(movie_info: BeautifulSoup, list_to_store_genres: list) -> str or None:
        """
        Function which gathers associated movie genres from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_genres: a list to store collected movie genres.
        :return: appends the associated movie genres to the selected list. If not provided None is returned.
        """
        try:
            movie_genres = movie_info.find('span', class_="genre").text.rstrip()[1:]
            return list_to_store_genres.append(str(movie_genres))
        except:
            return list_to_store_genres.append(np.nan)

    @staticmethod
    def get_movie_rating(movie_info: BeautifulSoup, list_to_store_rating: list) -> float or None:
        """
        Function which gathers movie IMDB rating from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_rating: a list to store collected movie rating.
        :return: appends the IMDB rating to the selected list. If not provided None is returned.
        """
        try:
            rating = movie_info.find('div', class_="inline-block ratings-imdb-rating")['data-value']
            return list_to_store_rating.append(float(rating))
        except:
            return list_to_store_rating.append(np.nan)

    @staticmethod
    def get_movie_metascore(movie_info: BeautifulSoup, list_to_store_metascore: list) -> int or None:
        """
        Function which gathers movie Metascore rating from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_metascore: a list to store collected Metascore rating.
        :return: appends Metascore rating to the selected list. If not provided None is returned.
        """
        try:
            metascore = movie_info.find('span', class_="metascore").text.rstrip()
            return list_to_store_metascore.append(int(metascore))
        except:
            return list_to_store_metascore.append(np.nan)

    @staticmethod
    def get_movie_votes(movie_info: BeautifulSoup, list_to_store_votes: list) -> int or None:
        """
        Function which gathers the number of votes from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_votes: a list to store collected number of votes.
        :return: appends the number of votes to the selected list. If not provided None is returned.
        """
        try:
            total_votes = movie_info.find('p', class_="sort-num_votes-visible").findChildren('span')[1]['data-value']
            return list_to_store_votes.append(int(total_votes))
        except:
            return list_to_store_votes.append(np.nan)

    @staticmethod
    def get_movie_box_office(movie_info: BeautifulSoup, list_to_store_box_office: list) -> int or None:
        """
        Function which gathers US box office earnings from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :param list_to_store_box_office: a list to store collected number of votes.
        :return: appends the US box office earnings to the selected list. If not provided None is returned.

        """
        try:
            box_office = movie_info.find('p', class_="sort-num_votes-visible").findChildren('span')[4][
                'data-value'].replace(',', '')
            return list_to_store_box_office.append(int(box_office))
        except:
            return list_to_store_box_office.append(np.nan)

    @staticmethod
    def get_movie_category(category: str, list_to_store_categories: list) -> str or None:
        """
        Function which takes the movie category and appends it to the list.

        :param category: category of the movie.
        :param list_to_store_categories: a list to store collected category names for movie.
        :return: appends the category name to the selected list.
        """
        try:
            return list_to_store_categories.append(str(category))
        except:
            return list_to_store_categories.append(np.nan)

    @staticmethod
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

    @staticmethod
    def write_to_csv(dataframe, title_of_csv_file: str):
        """
        Creates a csv file.

        :param dataframe: Pandas dataframe which should be used to create csv
        :param title_of_csv_file: desired csv file name
        :return: returns csv file
        """

        print(" >> Your csv file was created successfully << ")
        return dataframe.to_csv(f'{title_of_csv_file}.csv', index=None, header=True, na_rep=np.nan)

    @staticmethod
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

    def collect_information(self) -> pd.DataFrame:
        """

        :return:
        """
        title_list, page_list, year_list, certificate_list, runtime_list, \
        movie_genre_list, rating_list, metascore_list, total_votes_list, US_box_office_list, \
        category_list = ([] for i in range(11))

        main_category_list = self.collect_movie_categories()
        page_list = self.create_page_list()

        for genre in main_category_list:

            for page in page_list:

                all_movies_on_page = self.scrape_one_page(page=page, category=genre, timeout=self.timeout)

                for movie in all_movies_on_page:
                    self.get_movie_title(movie_info=movie, list_to_collect_titles=title_list)
                    self.get_movie_year(movie_info=movie, list_to_collect_movie_year=year_list)
                    self.get_movie_certificate(movie_info=movie, list_to_store_certificate=certificate_list)
                    self.get_movie_runtime(movie_info=movie, list_to_store_runtime=runtime_list)
                    self.get_movie_genres(movie_info=movie, list_to_store_genres=movie_genre_list)
                    self.get_movie_rating(movie_info=movie, list_to_store_rating=rating_list)
                    self.get_movie_metascore(movie_info=movie, list_to_store_metascore=metascore_list)
                    self.get_movie_votes(movie_info=movie, list_to_store_votes=total_votes_list)
                    self.get_movie_category(category=genre, list_to_store_categories=category_list)
                    self.get_movie_box_office(movie_info=movie, list_to_store_box_office=US_box_office_list)

        scraped_info = self.create_dictionary_for_movies(title=title_list,
                                                         release_year=year_list,
                                                         certificate=certificate_list,
                                                         runtime=runtime_list,
                                                         genres=movie_genre_list,
                                                         category=category_list,
                                                         rating=rating_list,
                                                         metascore=metascore_list,
                                                         votes=total_votes_list,
                                                         box_office=US_box_office_list)

        return self.create_dataframe_from_dictionary(scraped_info)

    def scrape_IMDB(self, number_of_movies_per_category: int, name_of_csv_file: str):
        self.number_of_movies_per_category = number_of_movies_per_category
        self.title_of_csv_file = name_of_csv_file
        IMDB_DataFrame = self.collect_information()
        self.write_to_csv(IMDB_DataFrame, self.title_of_csv_file)
        
