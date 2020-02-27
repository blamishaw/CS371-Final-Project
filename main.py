from scripts import movieWrapper


def create_interface():
    user_input = ""

    while user_input != 'n':
        user_input = input('Enter movie name:\n')
        movie = movieWrapper.Movie(user_input)
        if not movie.print_movies():
            continue
        user_input = input('Which movie is the correct one?\n')

        movie.get_movie(user_input)

        user_input = input("Do you want to continue? ('y'/'n')\n")


def main():
    create_interface()


if __name__ == '__main__':
    main()
