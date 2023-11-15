from dataclasses import dataclass

from postgres import Postgres


@dataclass
class flight:
    id: int
    flight_number: int
    arrival_airport: str
    departure_airport: str
    plane_type: str


def get_data_from_api():
    print("todo")


def write_data_into_db(db: Postgres, data: dict):
    db.run("INSERT INTO flights Values ("") ")


def get_data_from_db():
    print("todo")
