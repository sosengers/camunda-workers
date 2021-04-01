from camundaworkers.model.flight import Flight
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OfferMatch(Base):
    __tablename__ = 'offermatches'

    offer_code = Column(String(11), primary_key=True)

    outbound_flight_id = Column(Integer, ForeignKey("flights.id"))
    outbound_flight = relationship("Flight", primaryjoin=outbound_flight_id == Flight.id)

    comeback_flight_id = Column(Integer, ForeignKey("flights.id"))
    comeback_flight = relationship("Flight", primaryjoin=comeback_flight_id == Flight.id)

    blocked = Column(Boolean, default=False)