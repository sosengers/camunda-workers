from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Flight(Base):
    __tablename__ = 'flights'

    @staticmethod
    def from_json(flight_dict: dict):
        return Flight(
            flight_id=flight_dict.get('flight_id'),
            departure_airport_code=flight_dict.get('departure_airport_code'),
            arrival_airport_code=flight_dict.get('arrival_airport_code'),
            cost=flight_dict.get('cost'),
            departure_datetime=flight_dict.get('departure_datetime'),
            arrival_datetime=flight_dict.get('arrival_datetime'),
            flight_company_name="alitalia"
        )

    flight_id = Column(String(10), primary_key=True)
    departure_airport_code = Column(String(3))
    arrival_airport_code = Column(String(3))
    cost = Column(Float)
    departure_datetime = Column(DateTime, primary_key=True)
    arrival_datetime = Column(DateTime)
    flight_company_name = Column(String(50))
