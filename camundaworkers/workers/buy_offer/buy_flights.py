from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger


def buy_flights(task: ExternalTask) -> TaskResult:

    return task.complete()