from camunda.external_task.external_task import ExternalTask, TaskResult

from camundaworkers.logger import get_logger

import json
import pika


def send_tickets(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_tickets")

    user_communication_code = str(task.get_variable("user_communication_code"))
    tickets = str(task.get_variable("tickets"))
    logger.info(f"Tickets: {tickets}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="acmesky_mq"))
    channel = connection.channel()
    channel.queue_declare(queue=user_communication_code, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=user_communication_code,
        body=bytes(tickets, "utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()

    return task.complete()
