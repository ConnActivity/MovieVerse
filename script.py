import downloader
# import insert

all_movie_ids = set()
all_movies = []
PAGES = 10

for i in range(1, PAGES):
    all_movie_ids.update(
        movie.id
        for movie_list in [
            downloader.get_popular_movies(i).results,
            downloader.get_top_rated_movies(i).results,
            downloader.get_now_playing_movies(i).results,
        ]
        for movie in movie_list
    )

for movie_id in all_movie_ids:
    all_movies.append(downloader.get_movie_details(movie_id))
print(len(all_movies))
# insert.insert_movies(all_movies)
