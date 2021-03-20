from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def verify_payment_status(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("verify_payment_status")