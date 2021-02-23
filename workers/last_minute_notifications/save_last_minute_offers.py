from camunda.external_task.external_task import ExternalTask, TaskResult
import json
from model.base import create_sql_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError

from model.flight import Flight

import logging


def save_last_minute_offers(task: ExternalTask) -> TaskResult:
    Session = sessionmaker(bind=create_sql_engine())
    session = Session()
    print(task.get_variable("offers"))
    flights_dict = json.loads(task.get_variable("offers"))

    flights = [Flight.from_json(f) for f in flights_dict]

    print(flights)

    try:
        session.add_all(flights)
        session.commit()
    except DatabaseError:
        logging.error('ERROR: Error inserting rows in the database!')
        return task.bpmn_error(error_code='offer_saving_failed',
                               error_message='Error inserting rows in the database')

    return task.complete()
