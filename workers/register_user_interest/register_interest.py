from camunda.external_task.external_task import ExternalTask, TaskResult
import json
from pymongo import MongoClient

def register_interest(task: ExternalTask) -> TaskResult:

    interest = json.loads(task.get_variable("interest"))

    username = "root"
    password = "password"
    client = MongoClient(f"mongodb://{username}:{password}@acmesky_mongo:27017")
    acmesky_db = client['ACMESky']
    interests_collection = acmesky_db['interests']

    if not interests_collection.find_one(interest):
        interests_collection.insert_one(interest)

    return task.complete({"operation_result": "OK"})
