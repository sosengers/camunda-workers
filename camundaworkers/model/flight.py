from sqlalchemy import Column, String, DateTime, Float, Boolean, UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Flight(Base):
    __tablename__ = 'flights'

    @staticmethod
    def from_json(flight_dict: dict, flight_company: str):
        return Flight(
            flight_id=flight_dict.get('flight_id'),
            departure_airport_code=flight_dict.get('departure_airport_code'),
            arrival_airport_code=flight_dict.get('arrival_airport_code'),
            cost=flight_dict.get('cost'),
            departure_datetime=flight_dict.get('departure_datetime'),
            arrival_datetime=flight_dict.get('arrival_datetime'),
            flight_company_name=flight_company
        )

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(String(10))
    departure_airport_code = Column(String(3))
    arrival_airport_code = Column(String(3))
    cost = Column(Float)
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    flight_company_name = Column(String(50))

    __table_args__ = (
        UniqueConstraint('flight_id', 'departure_datetime'),
    )


class OfferMatch(Base):
    __tablename__ = 'offermatches'

    offer_code = Column(String(11), primary_key=True)

    outbound_flight_id = Column(Integer, ForeignKey("flights.id"))
    outbound_flight = relationship("Flight", primaryjoin=outbound_flight_id == Flight.id)

    comeback_flight_id = Column(Integer, ForeignKey("flights.id"))
    comeback_flight = relationship("Flight", primaryjoin=comeback_flight_id == Flight.id)

    blocked = Column(Boolean, default=False)
