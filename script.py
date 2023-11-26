import downloader

import insert

all_movie_ids = set()
all_movies = []
PAGES = 2
for i in range(1, PAGES):
    for movie in downloader.get_popular_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_top_rated_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_now_playing_movies(i).results:
        all_movie_ids.add(movie.id)
for movie_ids in all_movie_ids:
    all_movies.append(downloader.get_movie_details(movie_ids))
# insert.insert_movies(all_movies)
