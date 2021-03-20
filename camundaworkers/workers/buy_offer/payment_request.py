from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def payment_request(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("payment_request")