from sqlalchemy import Column, String, DateTime, Float, UniqueConstraint, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Flight(Base):
    __tablename__ = 'flights'

    @staticmethod
    def from_dict(flight_dict: dict, flight_company: str):
        return Flight(
            flight_code=flight_dict.get('flight_id'), # TODO sostituire nel JSON la chiave flight_id con flight_code
            departure_airport_code=flight_dict.get('departure_airport_code'),
            arrival_airport_code=flight_dict.get('arrival_airport_code'),
            cost=flight_dict.get('cost'),
            departure_datetime=flight_dict.get('departure_datetime'),
            arrival_datetime=flight_dict.get('arrival_datetime'),
            flight_company_name=flight_company
        )

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_code = Column(String(10))
    departure_airport_code = Column(String(3))
    arrival_airport_code = Column(String(3))
    cost = Column(Float)
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    flight_company_name = Column(String(50))

    __table_args__ = (
        UniqueConstraint('flight_code', 'departure_datetime'),
    )