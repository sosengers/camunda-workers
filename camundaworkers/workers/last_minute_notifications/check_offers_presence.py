from camunda.external_task.external_task import ExternalTask, TaskResult
import base64
import javaobj.v2 as javaobj
import json
from secrets import token_urlsafe

from camundaworkers.logger import get_logger
from camundaworkers.utils import *


def check_offers_presence(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("check_offers_presence")
    # task.get_variable('user') returns a marshalled base64 version of a java.util.HashMap
    # Therefore it needs to be decoded, deserialized, stringified and split on \n since every property
    # of the object seems to be on a different row.
    # Rows:
    # 0: type and address
    # 1: class name
    # 2: hex code
    # 3: key _id
    # 4: value of _id
    # 5: key interests
    # 6: value of interests
    deserialized_user = javaobj.loads(base64.b64decode(task.get_variable('user'))).dump().split('\n')

    user = deserialized_user[4].replace('\t', '').replace('\'', '')

    user_interests = json.loads(deserialized_user[6].replace('\t', '').replace('\'', '\"'))

    offers = json.loads(task.get_variable("offers"))

    offer_codes = []
    for interest in user_interests:
        outbound_flights = list(filter(lambda flight: departure_match_offer_interest(flight, interest), offers))
        comeback_flights = list(filter(lambda flight: comeback_match_offer_interest(flight, interest), offers))
        #logger.info(f"outbound_flights: {outbound_flights}")
        #logger.info(f"comeback_flights: {comeback_flights}")

        min_outbound_flight = min(outbound_flights, key=lambda flight: float(flight.get("cost")))
        min_comeback_flight = min(comeback_flights, key=lambda flight: float(flight.get("cost")))
        #logger.info(f"MIN  outbound_flights: {min_outbound_flight}")
        #logger.info(f"MIN comeback_flights: {min_comeback_flight}")

        if (float(min_outbound_flight.get("cost")) + float(min_comeback_flight.get("cost"))) <= float(interest.get("max_price")):
            offer_codes.append(str(token_urlsafe(8)))

    logger.info(f"Offer codes: {offer_codes}")
    return task.complete(global_variables={'offer_codes': json.dumps(offer_codes)})
