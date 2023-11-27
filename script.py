import time

import downloader
import insert

all_movie_ids = set()
all_movies = []
all_changes = []
PAGES = 1000

start_time = time.time()
for i in range(1, PAGES + 1):
    print(f"Page {i} of {PAGES} started")
    for movie in downloader.get_popular_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_top_rated_movies(i).results:
        all_movie_ids.add(movie.id)
    for movie in downloader.get_now_playing_movies(i).results:
        all_movie_ids.add(movie.id)
    for changes in downloader.get_changes_for_all_movies(i):
        all_movie_ids.add(changes["id"])
        all_changes.append(changes)
    print(f"Page {i} of {PAGES} finished")

end_time = time.time()
print(f"Iterating through pages took {end_time - start_time} seconds to complete")

all_movie_ids = {x for x in all_movie_ids if x is not None}

start_time = time.time()
print("Downloading movie details")
for i, movie_ids in enumerate(all_movie_ids):
    try:
        all_movies.append(downloader.get_movie_details(movie_ids))
    except Exception as e:
        print(f"Could not load movie with id {movie_ids}")
        print(e)
    if i % 25 == 0:
        print(f"{i} of {len(all_movie_ids)} loaded from API")

end_time = time.time()
print(f"Downloading details took {end_time - start_time} seconds to complete")

start_time = time.time()
print("Inserting movies into database")
for i, movie in enumerate(all_movies):
    try:
        insert.insert_movie(movie)
    except Exception as e:
        print(f"Could not insert movie with id {movie.id}")
        print(e)
    if i % 25 == 0:
        print(f"{i} of {len(all_movies)} inserted into database")

end_time = time.time()
print(f"Inserting movies took {end_time - start_time} seconds to complete")

start_time = time.time()
print("Inserting changes into database")
for changes in all_changes:
    for key, value in changes["changes"].items():
        try:
            insert.insert_movie_change(changes["id"], key, value)
        except Exception as e:
            print(f"Could not insert change for movie with id {changes['id']}")
            print(e)

end_time = time.time()
print(f"Inserting changes took {end_time - start_time} seconds to complete")
