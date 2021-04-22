from camunda.external_task.external_task import ExternalTask, TaskResult
import json
import pika

from camundaworkers.logger import get_logger


def send_result(task: ExternalTask) -> TaskResult:
    """
    Send through RabbitMQ the result message to the client
    :param task: the current task instance
    :return: the task result
    """
    logger = get_logger()
    logger.info("send_result")

    operation_result = task.get_variable("operation_result")
    interest = json.loads(task.get_variable("interest"))
    pg_username = interest.get("prontogram_username")

    """ Connect to RabbitMQ
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('acmesky_mq'))
    channel = connection.channel()

    """ Declare which queue will be used
    """
    channel.queue_declare(queue=pg_username, durable=True)

    """ Publish a message on the queue and close the connection
    """
    channel.basic_publish(exchange='',
                          routing_key=pg_username,
                          body=bytes(operation_result, 'utf-8'),
                          properties=pika.BasicProperties(delivery_mode=2)
                          )

    connection.close()

    return task.complete()
