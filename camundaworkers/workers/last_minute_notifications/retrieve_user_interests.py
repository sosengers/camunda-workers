from camunda.external_task.external_task import ExternalTask, TaskResult
from pymongo import MongoClient

from camundaworkers.logger import get_logger


def retrieve_user_interests(task: ExternalTask) -> TaskResult:
    """
    Retrieve from MongoDB the interests related to a user
    :param task: the current task instance
    :return: the task result
    """
    logger = get_logger()
    logger.info("retrieve_user_interests")

    """ Connect to MongoDB
    """
    username = "root"
    password = "password"
    client = MongoClient(f"mongodb://{username}:{password}@acmesky_mongo:27017")
    acmesky_db = client['ACMESky']
    interests_collection = acmesky_db['interests']

    """ Pipeline to perform the research and generate a clear dictionary with the data retrieved
    """
    pipeline = [
        {
            "$group": {
                "_id": "$prontogram_username",
                "interests": {
                    "$addToSet": {
                        "interest_id": "$_id",
                        "departure_airport_code": "$departure_airport_code",
                        "arrival_airport_code": "$arrival_airport_code",
                        "min_departure_date": "$min_departure_date",
                        "max_comeback_date": "$max_comeback_date",
                        "max_price": "$max_price",
                        "offer_codes": "$offer_codes"
                    }
                }
            }
        }
    ]

    users = list(interests_collection.aggregate(pipeline))

    for u in users:
        for i in u.get('interests'):
            # necessary since Camunda returns Java objects to be deserialized
            i['max_price'] = str(i['max_price'])
            i['interest_id'] = str(i['interest_id'])

    logger.info(f"There are {len(users)} users to be checked")
    return task.complete(global_variables={"users": users})
