import datetime
from typing import List, NamedTuple, Tuple

import psycopg2
from themoviedb.schemas import Movie, Person, Genre, Company
from themoviedb.schemas.countries import Country
from themoviedb.schemas.languages import Language

url = f"postgresql://postgres:postgres@49.13.1.33:5333/movie_db"

class MoviePopularity(NamedTuple):
    movie_id: int
    popularity: float
    vote_average: float


class MovieChange(NamedTuple):
    movie_id: int
    datapoint: str
    count: int


class MovieGenre(NamedTuple):
    movie_id: int
    genre_id: int


conn = psycopg2.connect(url)
cursor = conn.cursor()


def insert_movie(movies: List[Movie]):
    sql = """INSERT INTO movies 
            (id, title, original_title, imdb_id, overview, tagline, release_date, runtime, budget, 
            revenue, adult, video, backdrop_path, poster_path, homepage, status, original_language) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    movies_data = [(movie.id, movie.title, movie.original_title, movie.imdb_id, movie.overview, movie.tagline,
                    movie.release_date, movie.runtime, movie.budget, movie.revenue, movie.adult, movie.video,
                    movie.backdrop_path, movie.poster_path, movie.homepage, movie.status, movie.original_language)
                   for movie in movies]

    cursor.executemany(sql, movies_data)
    conn.commit()

    insert_movie_popularity([MoviePopularity(movie.id, movie.popularity, movie.vote_average) for movie in movies])
    insert_genre([genre for movie in movies for genre in movie.genres])
    insert_movie_genres([(movie.id, genre.id) for movie in movies for genre in movie.genres])

    for company in movie.production_companies:
        insert_production_company(company)
        insert_movie_production_companies(movie.id, company.id)

    for country in movie.production_countries:
        insert_country(country)
        insert_movie_production_countries(movie.id, country.iso_3166_1)

    for language in movie.spoken_languages:
        insert_spoken_language(language)
        insert_movie_spoken_languages(movie.id, language.iso_639_1)


def insert_movie_popularity(popularity_data: List[MoviePopularity]):
    sql = """INSERT INTO movies_popularity 
            (movie_id, popularity, vote_average, date) 
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (movie_id, date) DO NOTHING"""

    movie_popularity_data = [
        (popularity.movie_id, popularity.popularity, popularity.vote_average, datetime.date.today()) for popularity in
        popularity_data]

    cursor.executemany(sql, movie_popularity_data)
    conn.commit()


def insert_movie_change(movie_id: int, datapoint: str, count: int):
    sql = """INSERT INTO changes 
            (movie_id, datetime, datapoint, count)
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (movie_id, datetime, datapoint) DO NOTHING"""

    movie_change_data = (movie_id, datetime.date.today(), datapoint, count)

    cursor.execute(sql, movie_change_data)
    conn.commit()


def insert_genre(genres: List[Genre]):
    sql = """INSERT INTO genres 
            (id, name) 
            VALUES 
            (%s, %s) ON CONFLICT (id) DO NOTHING"""

    cursor.executemany(sql, genres)
    conn.commit()


def insert_movie_genres(movie_genres: List[Tuple[int, int]]):
    sql = """INSERT INTO moviegenres 
            (movie_id, genre_id) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, genre_id) DO NOTHING"""

    cursor.execute(sql, movie_genres)
    conn.commit()


def insert_production_company(company: Company):
    sql = """INSERT INTO productioncompanies 
            (id, name, logo_path, origin_country) 
            VALUES 
            (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    production_company_data = (company.id, company.name, company.logo_path, company.origin_country)

    cursor.execute(sql, production_company_data)
    conn.commit()


def insert_movie_production_companies(movie_id: int, production_company_id: int):
    sql = """INSERT INTO movieproductioncompanies 
            (movie_id, production_company_id) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, production_company_id) DO NOTHING"""

    movie_production_company_data = (movie_id, production_company_id)

    cursor.execute(sql, movie_production_company_data)
    conn.commit()


def insert_country(region: Country):
    sql = """INSERT INTO productioncountries 
            (iso_3166_1, name) 
            VALUES 
            (%s, %s) ON CONFLICT (iso_3166_1) DO NOTHING"""

    region_data = (region.iso_3166_1, region.name)

    cursor.execute(sql, region_data)
    conn.commit()


def insert_movie_production_countries(movie_id: int, country_code: str):
    # country code follows ISO 3166-1
    sql = """INSERT INTO movieproductioncountries 
            (movie_id, iso_3166_1) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, iso_3166_1) DO NOTHING"""

    movie_production_country_data = (movie_id, country_code)

    cursor.execute(sql, movie_production_country_data)
    conn.commit()


def insert_spoken_language(language: Language):
    sql = """INSERT INTO spokenlanguages 
            (iso_639_1, name, english_name) 
            VALUES 
            (%s, %s, %s) ON CONFLICT (iso_639_1) DO NOTHING"""

    language_data = (language.iso_639_1, language.name, language.english_name)

    cursor.execute(sql, language_data)
    conn.commit()


def insert_movie_spoken_languages(movie_id: int, language_code: str):
    # language code follows ISO 639-1
    sql = """INSERT INTO moviespokenlanguages 
            (movie_id, iso_639_1) 
            VALUES 
            (%s, %s) ON CONFLICT (movie_id, iso_639_1) DO NOTHING"""

    movie_spoken_language_data = (movie_id, language_code)

    cursor.execute(sql, movie_spoken_language_data)
    conn.commit()


def insert_person(person: Person):
    sql = """INSERT INTO people 
            (id, name, gender, known_for_department, profile_path, adult)
            VALUES 
            (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"""

    person_data = (
        person.id, person.name, person.gender, person.known_for_department, person.profile_path, person.adult)

    cursor.execute(sql, person_data)
    conn.commit()


def insert_person_popularity(person_id: int, popularity: float):
    sql = """INSERT INTO people_popularity 
            (person_id, popularity, date) 
            VALUES 
            (%s, %s, %s) ON CONFLICT (person_id, date) DO NOTHING"""

    person_popularity_data = (person_id, popularity, datetime.date.today())

    cursor.execute(sql, person_popularity_data)
    conn.commit()


def insert_known_works():
    ...
