from camundaworkers.model.purchase_process_information import PurchaseProcessInformation
import pika
import json
from camundaworkers.model.offer_purchase_data import OfferPurchaseData
from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def send_correct_offer_code(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_correct_offer_code")

    offer_purchase_data = OfferPurchaseData.from_dict(
        str(task.get_variable("offer_purchase_data"))
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters("acmesky_mq"))
    channel = connection.channel()

    queue_name = hash(offer_purchase_data)
    channel.queue_declare(queue=queue_name, durable=True)

    success = PurchaseProcessInformation(
        message=f"Il codice offerta {offer_purchase_data.offer_code} è valido."
    )

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=bytes(json.dumps(success.to_dict()), "utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()

    return task.complete()