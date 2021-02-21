from camunda.external_task.external_task import ExternalTask, TaskResult
import json
import pika

def send_result(task: ExternalTask) -> TaskResult:

    operation_result = task.get_variable("operation_result")
    interest = json.loads(task.get_variable("interest"))
    pg_username = interest.get("prontogram_username")

    connection = pika.BlockingConnection(pika.ConnectionParameters('acmesky_mq'))
    channel = connection.channel()

    channel.queue_declare(queue=pg_username, durable=True)

    channel.basic_publish(exchange='',
                      routing_key=pg_username,
                      body=bytes(operation_result, 'utf-8'),
                      properties=pika.BasicProperties(delivery_mode=2)
                      )

    connection.close()

    return task.complete()
