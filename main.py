import logging
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task_worker import ExternalTaskWorker

from workers.register_user_interest.tasks import TASKS as register_user_interest_TASKS
from workers.last_minute_notifications.tasks import TASKS as last_minute_notifications_TASKS

from model.flight import Base
from model.base import create_sql_engine

logger = logging.getLogger(__name__)

# configuration for the Client
default_config = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


def setup_logger():
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(threadName)s [%(levelname)s]: %(message)s"))
    logger.addHandler(ch)


def main():
    BASE_URL = "http://camunda_acmesky:8080/engine-rest"

    TOPICS = register_user_interest_TASKS + last_minute_notifications_TASKS

    # Setup PostgreSQL
    Base.metadata.create_all(create_sql_engine())

    executor = ThreadPoolExecutor(max_workers=len(TOPICS), thread_name_prefix="ACMESky-Backend")
    for index, topic_handler in enumerate(TOPICS):
        topic = topic_handler[0]
        handler_func = topic_handler[1]
        executor.submit(ExternalTaskWorker(worker_id=index, base_url=BASE_URL, config=default_config).subscribe, topic, handler_func)


if __name__ == '__main__':
    setup_logger()
    logger.info("Service running")
    main()
