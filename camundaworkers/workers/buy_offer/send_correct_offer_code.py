from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def send_correct_offer_code(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("send_correct_offer_code")