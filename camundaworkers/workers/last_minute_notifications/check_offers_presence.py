from camunda.external_task.external_task import ExternalTask, TaskResult
import base64
import javaobj.v2 as javaobj
import json

from camundaworkers.logger import get_logger


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

    return task.complete(global_variables={'offer_code': 'giovanni'})
