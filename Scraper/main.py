from Scraper import IMDB_scrapper as Scraper


def main():
    header = {'Turing-College-capstone-project-work': "Mozilla/5.0"}
    url_for_movie_genres = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"
    number_of_movies_per_category = 1
    title_of_csv_file = "scrape_test"

    main_category_list = Scraper.collect_movie_categories(url=url_for_movie_genres, header=header)
    print(" >> Genre list created successfully << ")

    movie_dataframe = Scraper.collect_information(number_of_items=number_of_movies_per_category,
                                                  main_category_list=main_category_list,
                                                  timeout=3,
                                                  header=header)

    Scraper.write_to_csv(movie_dataframe, title_of_csv_file)


if __name__ == "__main__":
    main()
