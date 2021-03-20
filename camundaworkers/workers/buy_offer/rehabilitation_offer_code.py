from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def rehabilitation_offer_code(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("rehabilitation_offer_code")