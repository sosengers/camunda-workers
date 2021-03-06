from camunda.external_task.external_task import ExternalTask, TaskResult
from pymongo import MongoClient

from camundaworkers.logger import get_logger

def retrieve_user_interests(task: ExternalTask) -> TaskResult:
    logger = get_logger()
    logger.info("retrieve_user_interests")

    username = "root"
    password = "password"
    client = MongoClient(f"mongodb://{username}:{password}@acmesky_mongo:27017")
    acmesky_db = client['ACMESky']
    interests_collection = acmesky_db['interests']

    pipeline = [
        {"$group": {
            "_id": "$prontogram_username",
            "interests": {
                "$addToSet": {
                    "departure_airport_code": "$departure_airport_code",
                    "arrival_airport_code": "$arrival_airport_code",
                    "min_departure_date": "$min_departure_date",
                    "max_comeback_date": "$max_comeback_date",
                    "max_price": "$max_price"
                }
            }
        }}
    ]

    users = list(interests_collection.aggregate(pipeline))

    for u in users:
        for i in u.get('interests'):
            i['max_price'] = str(i['max_price']) # necessary since Camunda returns Java objects to be deserialized

    logger.info(f"There are {len(users)} users to be checked")
    return task.complete(global_variables={"users": users})
