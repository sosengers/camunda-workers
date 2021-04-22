from camunda.external_task.external_task import ExternalTask, TaskResult
import json
from pymongo import MongoClient

from camundaworkers.logger import get_logger


def register_interest(task: ExternalTask) -> TaskResult:
    """
    Save the interest in MongoDB
    :param task: the current task instance
    :return: the task result
    """
    logger = get_logger()
    logger.info("register_interest")

    interest = json.loads(task.get_variable("interest"))
    interest["offer_codes"] = []

    """ Connection and save on MongoDB
    """
    username = "root"
    password = "password"
    client = MongoClient(f"mongodb://{username}:{password}@acmesky_mongo:27017") # Connect to MongoDB
    acmesky_db = client['ACMESky'] # Select the right DB
    interests_collection = acmesky_db['interests'] # Select the right document

    # Insert into the DB only if it does not already exist
    if not interests_collection.find_one(interest):
        interests_collection.insert_one(interest)

    return task.complete({"operation_result": "OK"})
