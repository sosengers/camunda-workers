from camundaworkers.model.flight import Flight, OfferMatch, PaymentTransaction
from camundaworkers.model.base import create_sql_engine
from camunda.external_task.external_task import ExternalTask, TaskResult
from sqlalchemy.orm.session import sessionmaker
from camundaworkers.logger import get_logger
from camundaworkers.model.offer_purchase_data import OfferPurchaseData

import json
import requests
from os import environ


def payment_request(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("payment_request")

    offer_purchase_data = OfferPurchaseData.from_dict(
        json.loads(task.get_variable("offer_purchase_data"))
    )

    offer_code = offer_purchase_data.offer_code

    Session = sessionmaker(bind=create_sql_engine())
    session = Session()

    offer_match = (
        session.query(OfferMatch)
        .filter(OfferMatch.offer_code == offer_code, OfferMatch.blocked == True)
        .first()
    )

    # affected_rows == 1 per precondizione.
    outbound_flight_id = offer_match.outbound_flight_id
    comeback_flight_id = offer_match.comeback_flight_id

    outbound_flight = session.query(Flight).filter(Flight.id == outbound_flight_id).first()
    comeback_flight = session.query(Flight).filter(Flight.id == comeback_flight_id).first()

    payment_request = {
        "amount": outbound_flight.cost + comeback_flight.cost,
        "payment_receiver": "ACMESky",
        "description": f"Il costo totale dell'offerta è: € {outbound_flight.cost + comeback_flight.cost}. I biglietti verranno acquistati dalla compagnia {outbound_flight.flight_company_name}.",
    }

    payment_provider_url = environ.get(
        "PAYMENT_PROVIDER_URL", "http://payment_provider_backend:8080"
    )

    payment_creation_response = requests.post(payment_provider_url + "/payments/request", json=payment_request)

    payment_tx = PaymentTransaction(
        transaction_id=payment_creation_response.json().get('transaction_id')
        )

    session.add(payment_tx)
    session.commit()

    return task.complete()
