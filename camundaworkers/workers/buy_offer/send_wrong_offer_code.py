from camundaworkers.model.purchase_error import PurchaseError
from camundaworkers.model.offer_purchase_data import OfferPurchaseData
from camunda.external_task.external_task import ExternalTask, TaskResult
import pika
import json
from camundaworkers.logger import get_logger


def send_wrong_offer_code(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_wrong_offer_code")

    offer_purchase_data = OfferPurchaseData.from_dict(str(task.get_variable("offer_purchase_data")))

    connection = pika.BlockingConnection(pika.ConnectionParameters('acmesky_mq'))
    channel = connection.channel()

    queue_name = hash(offer_purchase_data)
    channel.queue_declare(queue=queue_name, durable=True)

    error = PurchaseError(message=f"Il codice offerta {offer_purchase_data.offer_code} non è valido.")

    channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=bytes(json.dumps(error.to_dict()), 'utf-8'),
                      properties=pika.BasicProperties(delivery_mode=2)
                      )

    connection.close()

    return task.complete()