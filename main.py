import logging
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.client.engine_client import EngineClient

# configuration for the Client
default_config = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}

logger = logging.getLogger(__name__)

def setup_logger():
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(threadName)s [%(levelname)s]: %(message)s"))
    logger.addHandler(ch)

def handle_register_interest_task(task: ExternalTask) -> TaskResult:
    """
    """
    logger.info("Handle REGISTER INTEREST task")
    #logger.info("Global variables: {}".format(task.get_variables()))

    input_interest = task.get_variable("interest")

    print("Business logic here for handle_register_interest_task:)")

    return task.complete(global_variables={"operation_result": "Tutto ok"})

def handle_send_result_task(task: ExternalTask) -> TaskResult:
    """
    """
    logger.info("Handle SEND RESULT task")
    #logger.info("Global variables: {}".format(task.get_variables()))

    input_operation_result = task.get_variable("operation_result")

    print("Business logic for handle_send_result_task")

    return task.complete()

def main():
    BASE_URL = "http://camunda:8080/engine-rest"
    TOPICS = [
        ("register-interest", handle_register_interest_task),
        ("send-result", handle_send_result_task),
    ]

    executor = ThreadPoolExecutor(max_workers=len(TOPICS), thread_name_prefix="AcmeSky-Backend")
    for index, topic_handler in enumerate(TOPICS):
        topic = topic_handler[0]
        handler_func = topic_handler[1]
        executor.submit(ExternalTaskWorker(worker_id=index, base_url=BASE_URL, config=default_config).subscribe, topic, handler_func)


if __name__ == '__main__':
    setup_logger()
    logger.info("Service running")
    main()
