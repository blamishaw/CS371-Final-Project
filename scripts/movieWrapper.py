import tmdbsimple as tmdb
import apiconfig

# Dictionary to map tmdb genre ids to human-readable genres

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

        # All data in self.info is stored as a tuple(movie/person.id, movie/person.name)
        # id is stored for easy of querying tmdb API, name is stored for display/debugging purposes

        self.info = {
            'title': (None, None),
            'release_date': None,
            'genres': None,
            'director': (None, None),
            'cinematographer': (None, None),
            'actors': None,
        }

        search = tmdb.Search()

        # Movies with titles similar to or matching the user input string
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

            self.info['title'] = (self.movie['id'], self.movie['original_title'])
            self.info['release_date'] = self.movie['release_date']

            self.credits = tmdb.Movies(self.matches[int(number)-1]["id"]).credits()
        except IndexError:
            raise Exception('Index out of range')

    def getGenres(self):
        """ Gets the genre of movie """

        genres = [genre for genre in self.movie['genre_ids']]

        self.info['genres'] = genres

    def getDirector(self):
        """ Gets the director of the movie """

        for person in self.credits['crew']:
            if person['job'] == "Director":
                # Store director id and name in tuple
                self.info['director'] = (person['id'], person['name'])
                return

    def getCinematorgrapher(self):
        """ Gets the cinematographer ('Director of Photography') of the movie """

        for person in self.credits['crew']:
            if person['job'] == "Director of Photography":
                # Store cinematographer id and name
                self.info['cinematographer'] = (person['id'], person['name'])
                return


    def getActors(self):
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

    def convertInfoToKBFact(self):
        """ Converts self.info into facts that can be parsed by Companions """

        print('\n******** KB FACTS **********\n')
        kb_facts = []
        for key in self.info.keys():
            if key == 'title':
                fact = f'(title "{self.info[key][1]}")'
                kb_facts.append(fact)
            if key == 'release_date':
                fact = f'(releaseDate "{self.info["title"][1]}" {self.info[key]})'
                kb_facts.append(fact)
            if key == 'genres':
                for genre_id in self.info[key]:
                    fact = f'(genre "{self.info["title"][1]}" {GENRES[genre_id]})'
                    kb_facts.append(fact)
            if key == 'director':
                fact = f'(director "{self.info["title"][1]}" "{self.info[key][1]}"")'
                kb_facts.append(fact)
            if key == 'cinematographer':

                # Some animated movies don't have cinematographers
                if self.info[key][0] == None:
                    continue

                fact = f'(cinematographer "{self.info["title"][1]}" "{self.info[key][1]}"")'
                kb_facts.append(fact)
            if key == 'actors':
                for actor in self.info[key]:
                    fact = f'(actorIn "{self.info["title"][1]}" "{actor[1]}")'
                    kb_facts.append(fact)
        for item in kb_facts:
            print(item)

    def getInfo(self):
        """ Returns info about the movie in JSON format
        """
        print(self.info)
        print('\n')
