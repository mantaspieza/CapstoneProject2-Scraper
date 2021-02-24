##Introduction

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
`from Scraper.IMDB_scrapper import Scraper`
`scraper = Scraper()`

To start scraping just run the command:   
`scraper.scrape_IMDB()`

Scraper will scrape first 50 movies from each category collected from the page.
You can also input the desired number of movies to be scraped into scrape_IMDB function. (Note: each page contains 50 movies, therefore if 52 requested, the scraper will collect 100 movies per genre).

After scraping is complete, you will be provided with .csv file containing the scraped information. It is possible to input your .csv file name into scrape_IMDB function. (Default name: scraped_imdb_file.csv)

for more information just type help(Scraper)


## You can install it on your device  
#### note:    
You must have [pip](https://github.com/pypa/pip) installed on your device. follow the link for more information.    
To check whether pip is inslled type this:  
`pip --version`  

To install calculator to your device:  

`! pip install git+https://github.com/mantaspieza/IMDB_Movie_Scraper.git`


#### How to use calculator on your device:   

`python3`  
`from Scraper.IMDB_scrapper import Scraper`
`scraper = Scraper()`

To start scraping just run the command:   
`scraper.scrape_IMDB()`



