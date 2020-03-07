# CS371-Final-Project

Our goal, to create a movie recommendation algorithm using knowledge representation and reasoning. 

Our data, sourced from The Movie Database (TMDb), consists only of objective facts about a given movie. 
That is, we are not concerned with rating, popularity, or any other subjective metric. 

Our challenge, to reason about movie similarity based only on cast, crew, genre, and release year. We often found ourselves
asking, how can we break down what people like about certain movies into objective benchmarks?

To answer this question, we devised five qualities people use to determine similarity.

1. Aesthetic: The look of a movie – based on cinematography and genre
2. Plot: The script of a movie – based on writer and genre
3. Direction: The overall form and feel of a movie – based on director and release decade
4. Cast: The actors in a movie – self explanatory
5. Family Friendly: The accessible nature of the movie – based on Family ranking and animation status

## Project Structure

####Sub-Directories
* **krf**: The rules and predicates of the project
* **moviedata**: The knowledge base storing several hundred movies
* **scripts**: Python scripts to query the TMDb API, clean retrieved data, and store it in krf files

####Main Directory
* main.py: Python script to run the command line interface and parse user input
* To be created by user: apiconfig.py -- stores the TMDb API key


## Getting Started

###1. TMDb
To access the TMDb API as efficiently as possible we made use of the tmdbsimple Python module which can be downloaded as such:

`pip install tmdbsimple`

Likewise, one must get an API key from the TMDb website and store it in a file "apiconfig.py" in the main directory. This file should contain one line of the form:

`API_KEY = <<your api key>>`

API keys can be obtained [here](https://developers.themoviedb.org/3/getting-started/introduction).

###2. Companions

Our algorithm makes use of the Companions' interaction-manager to reason about movie similarity. That being said, Companions
needs a lot of movie data to even reason about in the first place, therefore we have provided a list of several
hundred movies in the "moviedata" directory.

Each krf file in this directory contains facts about ~200 movies totalling ~2800 facts per file. This takes a 
while to load in Companions and so to begin with, we recommend only using the first two krf files (enough to ensure
correctness of the algorithm). 

In addition, one should load "hornclauses.krf" and "moviepreds.krf" from the "krf" directory into 
Companions as well.

## Running the Algorithm

Once you have cloned the repository to your local machine, retrieved an API key and input it in the necessary file, and 
loaded the required flat files into Companions, you are ready to run the algorithm. 

To begin, open a new terminal window, navigate to the repository, and enter:

`python3 main.py`

After you have followed the prompts and received a Companions query there are two steps you must take:

1. Navigate to the "krf" directory and load "moviefacts.krf" into Companions. This ensures that
whatever movie you have selected is in the Companions database, regardless of if it was in the moviedata files
you initially uploaded.

2. Open the Companions Interaction-Manager and navigate to the Query page. In the context field, enter "MovieAlgorithmMt" 
and then paste the query returned by the command-line into the query box.

Naturally, some movies do not meet certain standards for the algorithm – our database just isn't large enough. For many 
movies however, Companions should return one or more movies that meet the required similarity definition.


