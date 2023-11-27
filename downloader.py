import datetime

from themoviedb import TMDb
import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer TOKEN "
}

api_key = "KEY"
tmdb = TMDb(key=api_key)


def get_popular_movies(page=1):
    movies = tmdb.movies().popular(page=page)
    return movies


def get_movie_details(movie_id):
    movie = tmdb.movie(movie_id).details()
    return movie


def get_movie_release_dates(movie_id):
    movie = tmdb.movie(movie_id)
    return movie.release_dates()


def get_alternative_titles(movie_id):
    movie = tmdb.movie(movie_id)
    return movie.alternative_titles()


def get_movie_change_list(page=1):
    url = f"https://api.themoviedb.org/3/movie/changes?page={page}&start_date={datetime.date.today() - datetime.timedelta(days=1)}&end_date={datetime.date.today()}"
    response = requests.get(url, headers=headers).json()
    response = response["results"]
    return response


def get_now_playing_movies(page=1):
    movies = tmdb.movies().now_playing(page=page)
    return movies


def get_popular_people():
    people = tmdb.people().popular()
    return people


def get_person_details(person_id):
    person = tmdb.person(person_id)
    return person


def get_top_rated_movies(page=1):
    movies = tmdb.movies().top_rated(page=page)
    return movies


def get_upcoming_movies(page=1):
    movies = tmdb.movies().upcoming(page=page)
    return movies


def get_changes_for_all_movies(page=1):
    changed_movies = get_movie_change_list(page)
    for movie in changed_movies:
        movie_id = movie["id"]
        changes = get_movie_changes(movie_id)
        movie["changes"] = changes

    return changed_movies


def get_movie_changes(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/changes?page=1"
    response = requests.get(url, headers=headers)
    response = response.json()
    change_list = response["changes"]

    changes = dict()

    for change in change_list:
        changes[change["key"]] = len(change["key"])

    return changes

