from .send_result import send_result
from .register_interest import register_interest

TASKS = [
    ("register-interest", register_interest),
    ("send-result", send_result)
]
