from camunda.external_task.external_task import ExternalTask, TaskResult

def send_result(task: ExternalTask) -> TaskResult:

    return task.complete()
