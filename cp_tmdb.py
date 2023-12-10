# copy tmdb
import os
import pickle
import concurrent.futures

import downloader

MOVIE_ID_LIMIT = 1250000
ROOT_PATH = ""


def download_movie_details(movie_id):
    if os.path.exists(f'{ROOT_PATH}/{movie_id}.pkl'):
        return
    try:
        movie = downloader.get_movie_details(movie_id)
        with open(f'{ROOT_PATH}/{movie_id}.pkl', 'wb') as f:
            pickle.dump(movie, f)
    except Exception as e:
        return


with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    future_movies = {executor.submit(download_movie_details, movie_id)
                     for movie_id in range(31700, MOVIE_ID_LIMIT + 1)}
