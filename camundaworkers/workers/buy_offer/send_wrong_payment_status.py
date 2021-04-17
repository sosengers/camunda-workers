import json
from camundaworkers.model.purchase_process_information import PurchaseProcessInformation
import pika
from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def send_wrong_payment_status(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_wrong_payment_status")

    user_communication_code = str(task.get_variable("user_communication_code"))

    connection = pika.BlockingConnection(pika.ConnectionParameters("acmesky_mq"))
    channel = connection.channel()

    channel.queue_declare(queue=user_communication_code, durable=True)

    error = PurchaseProcessInformation(
        message="Il processo di acquisto è fallito. Riprova nuovamente.",
        communication_code=user_communication_code,
        is_error=True,
    )

    channel.basic_publish(
        exchange="",
        routing_key=user_communication_code,
        body=bytes(json.dumps(error.to_dict()), "utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()

    return task.complete()