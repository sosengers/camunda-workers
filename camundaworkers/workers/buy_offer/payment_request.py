from camundaworkers.model.purchase_process_information import PurchaseProcessInformation
from camundaworkers.model.flight import Flight, OfferMatch, PaymentTransaction
from camundaworkers.model.base import create_sql_engine
from camunda.external_task.external_task import ExternalTask, TaskResult
from sqlalchemy.orm.session import sessionmaker
from camundaworkers.logger import get_logger
from camundaworkers.model.offer_purchase_data import OfferPurchaseData

import pika
import json
import requests
from os import environ


def payment_request(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("payment_request")

    user_communication_code = str(task.get_variable("user_communication_code"))

    offer_purchase_data = OfferPurchaseData.from_dict(
        json.loads(task.get_variable("offer_purchase_data"))
    )

    offer_code = offer_purchase_data.offer_code

    Session = sessionmaker(bind=create_sql_engine())
    session = Session()

    offer_match = session.query(OfferMatch).filter(OfferMatch.offer_code == offer_code,
                                                   OfferMatch.blocked == True).first()

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

    payment_provider_url = environ.get("PAYMENT_PROVIDER_URL", "http://payment_provider_backend:8080")

    payment_creation_response = requests.post(payment_provider_url + "/payments/request", json=payment_request).json()

    payment_tx = PaymentTransaction(transaction_id=payment_creation_response.get('transaction_id'))
    session.add(payment_tx)
    session.commit()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="acmesky_mq"))
    channel = connection.channel()
    channel.queue_declare(queue=user_communication_code, durable=True)

    purchase_url = PurchaseProcessInformation(message=str(payment_creation_response.get('redirect_page')))

    channel.basic_publish(
        exchange="",
        routing_key=user_communication_code,
        body=bytes(json.dumps(purchase_url.to_dict()), "utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()

    return task.complete()
