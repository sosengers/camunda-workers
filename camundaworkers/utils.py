from datetime import datetime, date

from camundaworkers.model.flight import Flight


def departure_match_offer_interest(offer: Flight, interest) -> bool:
    """
    Checks if the offers match the departure part of the interest.
    :param offer: a flight offer
    :param interest: an user interest
    :return: true if the offer match the departure part of the interest
    """
    # All'andata:

    # Se i due codici dell'aeroporto di partenza non coincidono non c'è un match
    if offer.departure_airport_code != interest.get("departure_airport_code"):
        return False

    # Se i due codici dell'aeroporto di arrivo non coincidono non c'è un match
    if offer.arrival_airport_code != interest.get("arrival_airport_code"):
        return False

    # Se la data minima nella quale l'utente vuole partire è minore della data di partenza del volo allora non c'è match
    if date.fromisoformat(interest.get("min_departure_date")) > offer.departure_datetime.date():
        return False

    return True


def comeback_match_offer_interest(offer: Flight, interest) -> bool:
    """
    Checks if the offers match the comeback part of the interest.
    :param offer: a flight offer
    :param interest: an user interest
    :return: ture if the offer match the comeback part of the interest
    """
    # Al ritorno, considerando lo stessa interesse inserito dall'utente

    # Se il codice di partenza dell'interessa è diverso dal codice di arrivo allora non c'è un match
    if offer.departure_airport_code != interest.get("arrival_airport_code"):
        return False

    # Se il codice di arrivo dell'interessa è diverso dal codice di partenza allora non c'è un match
    if offer.arrival_airport_code != interest.get("departure_airport_code"):
        return False

    # Se la data massima nella quale l'utente può tornare è minore della data del volo allora non c'è match

    if date.fromisoformat(interest.get("max_comeback_date")) < offer.arrival_datetime.date():
        return False

    return True
