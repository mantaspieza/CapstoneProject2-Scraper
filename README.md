## IMDB Movie Scraper

### Turing College Capstone Project part 1  

You can find Capstone Project part 2 ([IMDB Movie US Gross Profit Prediction API](https://github.com/mantaspieza/IMDB-gross-profit-prediction-api.git))

### Problem Description

As a person who enjoys movies i am always curious to know how much money would a movie make. I believe i share this curiousity together with other movie enthusiasts. It would be great to know it right?

### Goal of this project

The goal of this project is to collect data about the movies and to create a model which predicts the domestic movie earnings in US.

### About the data source

I have decided to scrape well known movie database [IMDB](https://www.imdb.com/?ref_=nv_home) and to collect information about the movies.

My scraper creates a list of current available movie categories (main genres).  
[click here to see main movie genres on IMDB](https://www.imdb.com/feature/genre/?ref_=nv_ch_gr)

And collects information about each listed movie in the category:
* Movie title
* Release year
* Certificate (age restrictions)
* Runtime
* genres of the movie
* IMDB rating
* Metascore rating
* Total number of votes
* US box office earnings.

## Installation and usage:    

#### You can easily run it in google colabs:  

`! pip install git+https://github.com/mantaspieza/IMDB_Movie_Scraper.git`  
`from scraper.scrape_imdb import Scraper`  
`scraper = Scraper()`  
  
To start scraping just run the command:   
`scraper.scrape_imdb()`

Enter minimum desired number of movies to be scraped per category. (Note: each page contains 50 movies, therefore if 52 requested, the scraper will collect 100 movies per genre).  
Enter desired name for the .csv file.

After scraping is complete, you will be provided with .csv file containing the scraped information.  
`Example:`  
``scraper.scrape_imdb(number_of_movies_per_category=1,
                    name_of_csv_file='scraped_imdb')``

For more information just type help(Scraper)


