import tmdbsimple as tmdb
import apiconfig

class PersonWrapper:

    tmdb.API_KEY = apiconfig.API_KEY

    def __init__(self, name):
        self.name = name
        self.info = None


