from scripts import tmdbWrapper

def createInterface():
    user_input = ""

    while user_input != 'n':
        user_input = input('Enter movie name:\n')
        movie = tmdbWrapper.MovieWrapper(user_input)
        if not movie.printMovies():
            return
        user_input = input('Which movie is the correct one?\n')

        movie.getMovie(user_input)
        movie.getGenres()
        movie.getDirector()
        movie.getActors()

        user_input = input("Do you want to continue? ('y'/'n')\n")

def main():
    createInterface()

if __name__ == '__main__':
    main()
