import downloader

import insert

all_movie_ids = set()
all_movies = []
all_changes_ids = set()
all_changes = []
PAGES = 2
for i in range(1, PAGES):
    for movie in downloader.get_popular_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_top_rated_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_now_playing_movies(i).results:
        all_movie_ids.add(movie.id)
    for changes in downloader.get_changes_for_all_movies(i):
        all_movie_ids.add(changes["id"])
        print(changes["id"])
        all_changes.append(changes)

all_movie_ids = {x for x in all_movie_ids if x is not None}

for movie_ids in all_movie_ids:
    print(movie_ids)
    all_movies.append(downloader.get_movie_details(movie_ids))

print(len(all_movies))

for movie in all_movies:
    insert.insert_movie(movie)

for changes in all_changes:
    for key, value in changes["changes"].items():
        insert.insert_movie_change(changes["id"], key, value)
