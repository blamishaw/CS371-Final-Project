import tmdbsimple as tmdb
import requests
import apiconfig

# Dictionary to map tmdb genre ids to human-readable genres

WRITE_TO_FILE = "krf/moviefacts.krf"
APPEND_TO_FILE = "krf/moviedata.krf"

GENRES = {28: "Action",
          12: "Adventure",
          16: "Animation",
          35: "Comedy",
          80: "Crime",
          99: "Documentary",
          18: "Drama",
          10751: "Family",
          14: "Fantasy",
          36: "History",
          27: "Horror",
          10402: "Musical",
          9648: "Mystery",
          10749: "Romance",
          878: "ScienceFiction",
          10770: "TVMovie",
          53: "Thriller",
          10752: "War",
          37: "Western",
        }

DECADES = {
    "11": "1910",
    "12": "1920",
    "13": "1930",
    "14": "1940",
    "15": "1950",
    "16": "1960",
    "17": "1970",
    "18": "1980",
    "19": "1990",
    "20": "2000",
    "21": "2010",
    "22": "2020",
}


class Movie:
    """ Wrapper for TMDb movie -- includes methods to get genre, director, actors, cinematographer, etc."""

    tmdb.API_KEY = apiconfig.API_KEY

    def __init__(self, user_input: str):
        """ Movie should be a user-input movie, while matches is a list of movies with similar titles"""
        self.input = user_input
        self.movie = None
        self.credits = None

        # All data in self.info is stored as a tuple(movie/person.id, movie/person.name)
        # id is stored for easy of querying tmdb API, name is stored for display/debugging purposes

        self.info = {
            'title': (None, None),
            'release_date': None,
            'genres': None,
            'director': (None, None),
            'cinematographer': (None, None),
            'composer': (None, None),
            'writer': (None, None),
            'actors': None,
        }

        search = tmdb.Search()

        # Movies with titles similar to or matching the user input string
        self.matches = search.movie(query=self.input)['results']

    def __repr__(self):
        print(self.matches)

    def print_movies(self) -> bool:
        """ Prints the movies with titles matching the user input """
        print("\n****************************************")

        if len(self.matches) == 0:
            print(f'No movies with name "{self.input}"')
            return False

        for i, movie in enumerate(self.matches):
            try:
                release_date = movie['release_date'][:4]
            except:
                release_date = "Unknown"
            print(f'{i+1}: {movie["original_title"]}, {release_date}')

        print("****************************************\n")
        return True

    def get_movie(self, number):
        """ This takes a number input by the user from the command line and then selects that movie as the correct title """
        if number.isalpha():
            raise Exception('Must enter a number')

        try:
            # Find the correct movie in self.matches based on user-input number
            self.movie = self.matches[int(number)-1]

            # Gets the credits of the movie for use in getDirector(), getComposer(), etc.
            self.credits = tmdb.Movies(self.matches[int(number)-1]["id"]).credits()

            # Calls self.getInfo() to populate the rest of the fields in self.info (i.e. director, actors, etc.)
            self.get_info()


        except IndexError:
            raise Exception('Index out of range')

    def set_movie(self, movie):
        self.movie = movie

        # Gets the credits of the movie for use in getDirector(), getComposer(), etc.
        self.credits = tmdb.Movies(self.movie["id"]).credits()

        # Calls self.getInfo() to populate the rest of the fields in self.info (i.e. director, actors, etc.)
        self.get_info()


    def get_title(self):
        """ Adds the movie id and original title to self.info """

        self.info['title'] = (self.movie['id'], self.movie['original_title'])

    def get_release_decade(self):
        """ Gets the decade the movie was released in and stores in self.info """

        release_decade = DECADES[self.movie['release_date'][0] + self.movie['release_date'][2]]
        self.info['release_date'] = release_decade

    def get_genres(self):
        """ Gets the genre of movie """

        genres = [genre for genre in self.movie['genre_ids']]
        self.info['genres'] = genres

    def get_crew_members(self):
        """ Gets the director, cinematographer, and composer of the movie """

        for person in self.credits['crew']:
            if person['job'] == "Director":
                # Store director id and name in tuple
                self.info['director'] = (person['id'], person['name'])
            if person['job'] == "Original Music Composer":
                # Store composer id and name
                self.info['composer'] = (person['id'], person['name'])
            if person['job'] == "Director of Photography":
                # Store cinematographer id and name
                self.info['cinematographer'] = (person['id'], person['name'])
            if person['job'] == "Screenplay":
                self.info['writer'] = (person['id'], person['name'])

    def get_actors(self):
        """ Gets the first 5 returned actors of the movie
            NOTE: this does not mean the 5 most popular or most "significant" actors in the movie
        """

        actors = []
        for i, character in enumerate(self.credits['cast']):
            if i < 5:
                # Store actor id and actor name
                actors.append((character['id'], character['name']))
            else:
                self.info['actors'] = actors
                return

    def convert_info_to_kb_facts(self) -> list:
        """ Converts self.info into facts that can be parsed by Companions """


        movie_title = self.info["title"][1]
        companions_id = "tmdb" + str(self.info["title"][0])

        kb_facts = []

        fact = f'(isa {companions_id} Movie-CW)'
        kb_facts.append(fact)

        fact = f'(movieTitleString {companions_id} "{movie_title}")'
        kb_facts.append(fact)



        for key in self.info.keys():
            if not self.info[key]:
                return []

            if not self.info[key][0]:
                continue

            if key == 'release_date':
                fact = f'(movieReleaseDecade {companions_id} {self.info[key]})'
                kb_facts.append(fact)

            if key == 'genres':
                for genre_id in self.info[key]:
                    if genre_id == 16:
                        fact = f'(movieIsAnimated {companions_id})'
                    else:
                        fact = f'(isa {companions_id} {GENRES[genre_id] + "Movie"})'
                    kb_facts.append(fact)

            if key == 'director':
                fact = f'(movieDirector {companions_id} "{self.info[key][1]}")'
                kb_facts.append(fact)

            if key == 'cinematographer':
                fact = f'(movieCinematographer {companions_id} "{self.info[key][1]}")'
                kb_facts.append(fact)

            if key == 'writer':
                fact = f'(movieWriter {companions_id} "{self.info[key][1]}")'
                kb_facts.append(fact)

            if key == 'composer':
                fact = f'(movieComposer {companions_id} "{self.info[key][1]}")'
                kb_facts.append(fact)

            if key == 'actors':
                for actor in self.info[key]:
                    fact = f'(movieActors {companions_id} "{actor[1]}")'
                    kb_facts.append(fact)

        return kb_facts

    def write_to_krf(self, kb_facts):
        """ Writes facts returned from self.convert_info_to_kb_facts to krf file """

        file = open(WRITE_TO_FILE, "w")
        for fact in kb_facts:
            file.write(fact + '\n')
        file.close()

    def append_to_krf(self, kb_facts):
        """ This function is only invoked when adding movies to moviedata.krf """

        file = open(APPEND_TO_FILE, "a")
        for fact in kb_facts:
            file.write(fact + '\n')
        file.write('\n\n')
        file.close()

    def get_info(self):
        """ Load all info about the movie in JSON format
        """
        self.get_title()
        self.get_release_decade()
        self.get_genres()
        self.get_crew_members()
        self.get_actors()
        kb_facts = self.convert_info_to_kb_facts()
        self.append_to_krf(kb_facts)
        print(f"Copy and paste to Companions: (recommendMovie {'tmdb' + str(self.info['title'][0])} ?movie2)")


        # self.write_to_krf(kb_facts)


def get_all_movies():
    """ Function to add more movies to our database, we have already parsed the first 100 pages of the most popular movies
        on TMDb. This has given us over 30,000 lines of facts and about 2,000 unique movies for our KB. Given a more
        scalable system, we would naturally include all 500 pages of movies, but for the purposes of this assignment
        100 pages is likely enough.
    """

    # This is accessed using an actual API connection as opposed to using the tmdbsimple module
    api_key = apiconfig.API_KEY

    # Start on page 101 as the first 100 pages are already included in moviedata.krf
    page_num = 1

    while page_num <= 500:
        print(page_num)
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=' + api_key + '&certification_country=US&certification.lte=G&sort_by=popularity.desc&page=' + str(page_num))
        all_movies = response.json()
        for movie in all_movies['results']:
            Movie(movie).set_movie(movie)
        page_num += 1
