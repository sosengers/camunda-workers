from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def verify_offer_code_validity(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("verify_offer_code_validity")