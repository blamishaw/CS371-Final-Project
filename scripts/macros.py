WRITE_TO_FILE = "krf/moviefacts.krf"
APPEND_TO_FILE = "moviedata/movie-data2.krf"

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

REASONING_CRITERIA = [
    'similarAesthetic',
    'similarPlot',
    'similarDirection',
    'similarCast',
    'isFamilyFriendly'
]