from camunda.external_task.external_task import ExternalTask, TaskResult
import requests
import json

from camundaworkers.logger import get_logger


def notify_user_via_prontogram(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("notify_user_via_prontogram")

    offer_codes = json.loads(task.get_variable("offer_codes"))
    prontogram_username = str(task.get_variable("prontogram_username"))[1:-1] # '' are added at the beggin and at the end of the pg_username, [1:-1] removes them
    logger.info(f"prontogram username: {prontogram_username}")
    logger.info(f"offer codes: {offer_codes}")

    for offer_code in offer_codes:
        prontogram_message = {
            "sender": "ACMESky",
            "receiver": prontogram_username,
            "body": f"Il tuo codice offerta è: {offer_code}. Affrettati, sarà valido per sole 24 ore!"
        }

        #logger.info(json.dumps(prontogram_message))
        r = requests.post("http://prontogram_backend:8080/messages", json=prontogram_message)

        logger.info(f"ProntoGram response: {r.status_code}")
        if r.status_code >= 300:
            logger.warn(r.text)
    return task.complete()
