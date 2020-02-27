import tmdbsimple as tmdb
import apiconfig

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
          10402: "Music",
          9648: "Mystery",
          10749: "Romance",
          878: "Science Fiction",
          10770: "TV Movie",
          53: "Thriller",
          10752: "War",
          37: "Western",
        }


class Movie:
    """ Wrapper for TMDB movie -- includes methods to get genre, director, actors, cinematographer, etc."""

    tmdb.API_KEY = apiconfig.API_KEY

    def __init__(self, user_input: str):
        """ Movie should be a user-input movie, while matches is a list of movies with similar titles"""
        self.input = user_input
        self.movie = None
        self.credits = None

        # All data is stored by their tmdb ids for ease of querying the API
        self.info = {
            'title': None,
            'release_date': None,
            'genres': None,
            'director': None,
            'cinematographer': None,
            'actors': None,
        }

        search = tmdb.Search()
        self.matches = search.movie(query=self.input)['results']


    def __repr__(self):
        print(self.matches)

    def printMovies(self):
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


    def getMovie(self, number):
        """ This takes a number input by the user from the command line and then selects that movie as the correct title"""
        if number.isalpha():
            raise Exception('Must enter a number')

        try:
            self.movie = self.matches[int(number)-1]

            self.info['title'] = self.movie['id']
            self.info['release_date'] = self.movie['release_date']

            self.credits = tmdb.Movies(self.matches[int(number)-1]["id"]).credits()
        except IndexError:
            raise Exception('Index out of range')

    def getGenres(self):
        """ Gets the genre of movie """

        print("\n********* GENRES ************")
        genres = []
        for genre in self.movie['genre_ids']:
            genres.append(genre)
            print(GENRES[genre])
        print("*****************************\n")
        self.info['genres'] = genres

    def getDirector(self):
        """ Gets the director of the movie """

        print("********* DIRECTOR **********")
        for person in self.credits['crew']:
            if person['job'] == "Director":
                print(f"{person['name']}")
                print("*****************************\n")
                self.info['director'] = person['id']
                return

    def getCinematorgrapher(self):
        """ Gets the cinematographer ('Director of Photography') of the movie """

        print("****** CINEMATOGRAPHER ******")
        for person in self.credits['crew']:
            if person['job'] == "Director of Photography":
                print(f"{person['name']}")
                print("*****************************\n")
                self.info['cinematographer'] = person['id']
                return

    def getActors(self):
        """ Gets the first 5 returned actors of the movie
            NOTE: this does not mean the 5 most popular or most "significant" actors in the movie
        """
        print("********* ACTORS ************")
        actors = []
        for i, character in enumerate(self.credits['cast']):
            if i < 5:
                print(character['name'])
                actors.append(character['id'])
            else:
                print("*****************************\n")
                self.info['actors'] = actors
                return

    def getInfo(self):
        """ Returns info about the movie in JSON format
        """
        print(self.info)
        print('\n')
