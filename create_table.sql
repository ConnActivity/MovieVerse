CREATE TABLE Movies (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    original_title VARCHAR(255),
    imdb_id VARCHAR(20),
    overview TEXT,
    tagline VARCHAR(255),
    release_date DATE,
    runtime INT,
    budget DECIMAL(15, 2),
    revenue DECIMAL(15, 2),
    adult BOOLEAN,
    video BOOLEAN,
    backdrop_path VARCHAR(255),
    poster_path VARCHAR(255),
    homepage VARCHAR(255),
    status VARCHAR(50),
    original_language VARCHAR(10)
);

CREATE TABLE Genres (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE ProductionCompanies (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    logo_path VARCHAR(255),
    origin_country VARCHAR(5)
);

CREATE TABLE ProductionCountries (
    iso_3166_1 VARCHAR(5) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE SpokenLanguages (
    iso_639_1 VARCHAR(5) PRIMARY KEY,
    name VARCHAR(255),
    english_name VARCHAR(255)
);

CREATE TABLE MovieGenres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(id),
    FOREIGN KEY (genre_id) REFERENCES Genres(id)
);
CREATE TABLE MovieProductionCompanies (
    movie_id INT,
    production_company_id INT,
    PRIMARY KEY (movie_id, production_company_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(id),
    FOREIGN KEY (production_company_id) REFERENCES ProductionCompanies(id)
);

CREATE TABLE MovieProductionCountries (
    movie_id INT,
    iso_3166_1 VARCHAR(5),
    PRIMARY KEY (movie_id, iso_3166_1),
    FOREIGN KEY (movie_id) REFERENCES Movies(id),
    FOREIGN KEY (iso_3166_1) REFERENCES ProductionCountries(iso_3166_1)
);

CREATE TABLE MovieSpokenLanguages (
    movie_id INT,
    iso_639_1 VARCHAR(5),
    PRIMARY KEY (movie_id, iso_639_1),
    FOREIGN KEY (movie_id) REFERENCES Movies(id),
    FOREIGN KEY (iso_639_1) REFERENCES SpokenLanguages(iso_639_1)
);

CREATE TABLE Changes (
    movie_id INT,
    datetime date,
    datapoint VARCHAR(255),
    PRIMARY KEY (movie_id, datetime, datapoint),
    FOREIGN KEY (movie_id) REFERENCES Movies(id),
    count INT
);

CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    gender INTEGER,
    known_for_department VARCHAR(50),
    profile_path VARCHAR(255),
    adult BOOLEAN
);

CREATE TABLE known_works (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    adult BOOLEAN,
    backdrop_path VARCHAR(255),
    title VARCHAR(100),
    original_language VARCHAR(10),
    original_title VARCHAR(100),
    overview TEXT,
    poster_path VARCHAR(255),
    media_type VARCHAR(50),
    popularity NUMERIC(10,3),
    release_date DATE,
    video BOOLEAN,
    vote_average NUMERIC(3,1),
    vote_count INTEGER,
    genre_ids INTEGER[]
);

CREATE TABLE movies_popularity (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id),
    popularity NUMERIC(10,3),
    vote_average NUMERIC(3,1),
    date DATE,
    CONSTRAINT movies_popularity_movie_id_date_key UNIQUE (movie_id, date)
);

CREATE TABLE people_popularity (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    popularity NUMERIC(10,3),
    vote_average NUMERIC(3,1),
    date DATE
);