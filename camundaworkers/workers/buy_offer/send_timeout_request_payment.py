from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def send_timeout_request_payment(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_timeout_request_payment")