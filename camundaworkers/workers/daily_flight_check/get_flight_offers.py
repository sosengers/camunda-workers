from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger
import requests
from json import dumps


def get_flight_offers(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("get_flight_offers")

    url = task.get_variable("company")
    logger.info("Contacting: " + url)

    new_flights = requests.get(url + "/flights/offers").json()

    if new_flights == {}:
        logger.info("Empty json from flight company")
        return task.complete({'offers': dumps([])})
    else:
        return task.complete({'offers': dumps(new_flights.get('flights'))})
