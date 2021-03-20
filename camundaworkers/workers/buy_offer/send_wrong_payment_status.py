from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def send_wrong_payment_status(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_wrong_payment_status")