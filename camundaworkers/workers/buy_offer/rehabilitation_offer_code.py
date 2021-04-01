from camunda.external_task.external_task import ExternalTask, TaskResult
from camundaworkers.logger import get_logger
from sqlalchemy.orm.session import sessionmaker
from camundaworkers.logger import get_logger
from camundaworkers.model.base import create_sql_engine
from camundaworkers.model.flight import OfferMatch


def rehabilitation_offer_code(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("rehabilitation_offer_code")

    offer_code = str(task.get_variable("offer_code"))

    Session = sessionmaker(bind=create_sql_engine())
    session = Session()

    affected_rows = session.query(OfferMatch).filter(OfferMatch.offer_code == offer_code).update({"blocked": False}, synchronize_session="fetch")
    if affected_rows < 1:
        session.rollback() # TODO verificare se è necessario
        logger.error(f"{affected_rows} matches were found for the given offer code. The offer code will not be rehabilitated.")
        return task.complete()

    logger.info(f"{affected_rows} match was found for the given offer code.")
    session.commit()
    return task.complete()