from camundaworkers.model.offer_purchase_data import OfferPurchaseData
from camundaworkers.model.flight import OfferMatch
from camunda.external_task.external_task import ExternalTask, TaskResult
from sqlalchemy.orm.session import sessionmaker
from camundaworkers.logger import get_logger
from camundaworkers.model.base import create_sql_engine

import json


def verify_offer_code_validity(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("verify_offer_code_validity")

    offer_purchase_data = OfferPurchaseData.from_dict(json.loads(task.get_variable("offer_purchase_data")))

    offer_code = offer_purchase_data.offer_code

    Session = sessionmaker(bind=create_sql_engine())
    session = Session()

    user_communication_code = str(hash(offer_purchase_data))
    affected_rows = session.query(OfferMatch).filter(OfferMatch.offer_code == offer_code).update({"blocked": True}, synchronize_session="fetch")
    if affected_rows < 1:
        session.rollback() # TODO verificare se è necessario
        logger.error(f"{affected_rows} matches were found for the given offer code.")
        return task.complete(global_variables={'offer_code_validity': False, 'user_communication_code': user_communication_code})

    logger.info(f"{affected_rows} match was found for the given offer code.")
    session.commit()
    return task.complete(global_variables={'offer_code_validity': True, 'user_communication_code': user_communication_code})