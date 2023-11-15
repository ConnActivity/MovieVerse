-- TODO: Fill in useful columns
Create table flights (
    id serial primary key,
    flight_number varchar(10) not null,
    arrival_airport varchar(3) not null constraint airports_fk references airports(airport_code),
    departure_airport varchar(3) not null,
    plane_type varchar(24) not null,
    departure_time timestamp not null,
    arrival_time timestamp not null,
    departure_runway timestamp,
    arrival_runway timestamp
);

CREATE table flight_data (
    id serial primary key,
    flight_number varchar(10) not null constraint flights_fk references flights(flight_number),
    speed int not null,
    heading int not null,
    barometric_altitude int not null,
    gps_altitude int not null,
    latitude float not null,
    longitude float not null,
    time timestamp not null,
    -- Unknown data types
    wind VARCHAR(8),
    temperature int
);

CREATE table airports (
    airport_code varchar(3) not null primary key,
    airport_name varchar(100) not null,
    city varchar(100) not null,
    country varchar(100) not null,
    latitude float not null,
    longitude float not null
);

CREATE table runway (
    id serial primary key,
    airport_code varchar(3) not null constraint airports_fk references airports(airport_code),
    runway_number varchar(10) not null,
    runway_length int not null,
    runway_width int not null
);

CREATE table geofence (
    id serial primary key,
    airport_code varchar(3) not null constraint airports_fk references airports(airport_code),
    label varchar(20) not null,
    latitude_sw float not null,
    longitude_sw float not null,
    latitude_ne float not null,
    longitude_ne float not null
);

