import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd
import time
import numpy as np
from typing import Union


class Scraper(object):
    def __init__(
        self,
        id: str = "Turing-College-capstone-project-work",
        web_browser: str = "Mozilla/5.0",
        url_for_movie_categories: str = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr",
        number_of_movies_per_category: int = 1,
        title_of_csv_file: str = "scraped_imdb_file",
        timeout: int = 2,
    ):
        """
        Initialization

        :param id: Id used to construct scraper headers.
        :param web_browser: web browser information used to construct scraper headers.
        :param url_for_movie_categories: Url used to collect movie categories for scraping.
        :param number_of_movies_per_category: default is set to 1.
        :param title_of_csv_file: Default "scraped_imdb_file"
        :param timeout: Time duration between the page iteration not to spam IMDB server.
        """
        self.header = {id: web_browser}
        self.url_for_movie_categories = url_for_movie_categories
        self.number_of_movies_per_category = number_of_movies_per_category
        self.title_of_csv_file = title_of_csv_file
        self.timeout = timeout
        self.list = []

    def get_page_response(self, url: str, header: dict) -> BeautifulSoup:
        """
        Retrieves response from IMDB server.

        :param url: desired url.
        :param header: identification needed for scraping. constructed during Initialization.
        :return: response. if connection blocked prints error message.
        """
        self.response = requests.get(url, headers=header)
        soup = BeautifulSoup(self.response.text, "html.parser")
        if not self.response.ok:
            print(f"There is an {self.response} error")
        else:
            return soup

    def collect_movie_categories(self) -> list:
        """
        Scrapes IMDB movie categories.
        :return: list with all categories from IMDB.
        """
        soup = self.get_page_response(
            url=self.url_for_movie_categories, header=self.header
        )

        all_categories = soup.find_all("div", class_="widget_image")

        return [movie_genre.find("img")["title"] for movie_genre in all_categories]

    def create_page_list(self) -> list:
        """
        Creates a list with movie ID required to iterate through the IMDB pages.
        :return: list containing required movie IDs
        """
        page_list = []
        for item in range(1, self.number_of_movies_per_category + 1, 50):
            page_list.append(item)
        return page_list

    def scrape_one_page(
        self, category: str, page: int, timeout: float
    ) -> ResultSet:
        """
        Takes the category and movie id from lists, updates the base url with this information and scrapes
        the required information.

        :param category: category required to construct the URL for scraping
        :param page: movie ID required to construct the URL for scraping.
        :param timeout: Time duration between the page iteration not to spam IMDB server.
        :return:
        """

        print(f"Now scraping {category} movies from page starting with movie id {page}")

        url = f"https://www.imdb.com/search/title/?genres={category}&sort=boxoffice_gross_us,desc&start={page}&explore=title_type,genres&ref_=adv_nxt"
        soup = self.get_page_response(url=url, header=self.header)

        all_movies_on_page = soup.find_all("div", class_="lister-item")

        time.sleep(timeout)
        return all_movies_on_page

    @staticmethod
    def get_movie_title(movie_info: BeautifulSoup) -> Union[str or None]:
        """
        Function which gathers movie title from the provided BeautifulSoup object.

        :param movie_info: BeautifulSoup object containing movie info.
        :return: appends the title to the selected list. If not provided None is returned.
        """

        try:
            title = movie_info.find("span", class_="lister-item-index").find_next().text
            if title is None:
                return np.nan
            return str(title)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_year(
        movie_info: BeautifulSoup,
    ) -> Union[int or None]:
        """
        Function which gathers movie release year from the provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing movie info.
        :return: appends the movie release year to selected list. If not provided None is returned.
        """
        try:
            # Slices the result to take only numeric value
            year = movie_info.find("span", class_="lister-item-year").text[1:5]
            if year is None:
                return np.nan
            else:
                return int(year)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_certificate(
        movie_info: BeautifulSoup,
    ) -> Union[str or None]:
        """
        Function which gathers movie certificate(age restrictions) from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends the movie certificate to selected list. If not provided None is returned.
        """
        try:
            certificate = movie_info.find("span", class_="certificate").text
            if certificate is None:
                return np.nan
            return str(certificate)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_runtime(
        movie_info: BeautifulSoup,
    ) -> Union[str or None]:
        """
        Function which gathers runtime of the movie from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie
        :return: appends the runtime of the movie to selected list. If not provided None is returned.
        """
        try:
            runtime = movie_info.find("span", class_="runtime").text
            if runtime is None:
                return np.nan
            return str(runtime)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_genres(
        movie_info: BeautifulSoup,
    ) -> Union[str or None]:
        """
        Function which gathers associated movie genres from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends the associated movie genres to the selected list. If not provided None is returned.
        """
        try:
            # Slices result and removes excessive white spaces
            movie_genres = movie_info.find("span", class_="genre").text.rstrip()[1:]
            if movie_genres is None:
                return np.nan
            return str(movie_genres)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_rating(movie_info: BeautifulSoup) -> Union[float or None]:
        """
        Function which gathers movie IMDB rating from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends the IMDB rating to the selected list. If not provided None is returned.
        """
        try:
            rating = movie_info.find("div", class_="inline-block ratings-imdb-rating")[
                "data-value"
            ]
            if rating is None:
                return np.nan
            return float(rating)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_metascore(movie_info: BeautifulSoup) -> Union[int or None]:
        """
        Function which gathers movie Metascore rating from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends Metascore rating to the selected list. If not provided None is returned.
        """
        try:
            # Removes excessive white spaces
            metascore = movie_info.find("span", class_="metascore").text.rstrip()
            if metascore is None:
                return np.nan
            return int(metascore)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_votes(movie_info: BeautifulSoup) -> Union[int or None]:
        """
        Function which gathers the number of votes from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends the number of votes to the selected list. If not provided None is returned.
        """
        try:
            total_votes = movie_info.find(
                "p", class_="sort-num_votes-visible"
            ).findChildren("span")[1]["data-value"]
            if total_votes is None:
                return np.nan
            return int(total_votes)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_box_office(movie_info: BeautifulSoup) -> Union[int or None]:
        """
        Function which gathers US box office earnings from provided BeautifulSoup info.

        :param movie_info: BeautifulSoup object containing info about the movie.
        :return: appends the US box office earnings to the selected list. If not provided None is returned.

        """
        try:
            box_office = (
                movie_info.find("p", class_="sort-num_votes-visible")
                .findChildren("span")[4]["data-value"]
                .replace(",", "")
            )
            if box_office is None:
                return np.nan
            return int(box_office)
        except ValueError:
            return np.nan

    @staticmethod
    def get_movie_category(category: str) -> Union[str or None]:
        """
        Function which takes the movie category and appends it to the list.

        :param category: category of the movie.
        :return: appends the category name to the selected list.
        """
        try:
            if category is None:
                return np.nan
            return str(category)
        except ValueError:
            return np.nan

    @staticmethod
    def write_to_csv(dataframe, title_of_csv_file: str) -> None:
        """
        Creates a csv file.

        :param dataframe: Pandas dataframe which should be used to create csv
        :param title_of_csv_file: desired csv file name
        :return: returns csv file
        """

        print(" >> Your csv file was created successfully << ")
        return dataframe.to_csv(
            f"{title_of_csv_file}.csv", index=None, header=True, na_rep=np.nan
        )

    def collect_information(self) -> pd.DataFrame:
        """
        Function which combines all functions required for scraping.

        :return: Pandas DataFrame.
        """

        main_category_list = self.collect_movie_categories()
        page_list = self.create_page_list()

        for genre in main_category_list:

            for page in page_list:

                all_movies_on_page = self.scrape_one_page(
                    page=page, category=genre, timeout=self.timeout
                )

                for movie in all_movies_on_page:

                    self.list.append(
                        {
                            "title": self.get_movie_title(movie_info=movie),
                            "year": self.get_movie_year(movie_info=movie),
                            "certificate": self.get_movie_certificate(movie_info=movie),
                            "length": self.get_movie_runtime(movie_info=movie),
                            "genres": self.get_movie_genres(movie_info=movie),
                            "rating": self.get_movie_rating(movie_info=movie),
                            "metascore": self.get_movie_metascore(movie_info=movie),
                            "total_votes": self.get_movie_votes(movie_info=movie),
                            "category": self.get_movie_category(category=genre),
                            "US_box_office": self.get_movie_box_office(
                                movie_info=movie
                            ),
                        }
                    )

        return pd.DataFrame(self.list)

    def scrape_imdb(
        self, number_of_movies_per_category: int, name_of_csv_file: str
    ) -> None:
        """
        Function which is used to activate the scraper.

        :param number_of_movies_per_category: desired number of movies per category to be scraped. default = 1
        :param name_of_csv_file: desired name of csv file. default = "scraped_imdb_file"
        :return: CSV file is created in project directory.
        """
        self.number_of_movies_per_category = number_of_movies_per_category
        self.title_of_csv_file = name_of_csv_file
        self.write_to_csv(self.collect_information(), self.title_of_csv_file)

