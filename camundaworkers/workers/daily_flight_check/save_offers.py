from camunda.external_task.external_task import ExternalTask, TaskResult

from camundaworkers.model.base import create_sql_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError

from camundaworkers.logger import get_logger

from camundaworkers.model.flight import Flight

from json import loads


def save_offers(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("save_offers")

    Session = sessionmaker(create_sql_engine())
    session = Session()

    company_url = task.get_variable('company')
    # Workaround: Camunda string global variables can hold maximum 4000 chars per string.
    # Therefore we must concatenate the dumped strings.
    offers_packets = int(task.get_variable('offers_packets'))
    offers = ""
    for packet in range(offers_packets):
        offers += task.get_variable(f'offers_{packet}')
    
    today_flights = [Flight.from_dict(flight_json, company_url) for flight_json in loads(offers)]

    try:
        session.add_all(today_flights)
        session.commit()
        logger.info(f"Added {len(today_flights)} flights to acmesky_db from {company_url}")
    except DatabaseError:
        logger.warn(f"Database error while inserting {len(today_flights)} from {company_url}")
        return task.bpmn_error(error_code='offer_saving_failed',
                               error_message='Error inserting rows in the database')

    return task.complete()
