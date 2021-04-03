from camundaworkers.workers.buy_offer.payment_request import payment_request
from camundaworkers.workers.buy_offer.rehabilitation_offer_code import rehabilitation_offer_code
from camundaworkers.workers.buy_offer.send_correct_offer_code import send_correct_offer_code
from camundaworkers.workers.buy_offer.send_timeout_request_payment import send_timeout_request_payment
from camundaworkers.workers.buy_offer.send_wrong_offer_code import send_wrong_offer_code
from camundaworkers.workers.buy_offer.send_wrong_payment_status import send_wrong_payment_status
from camundaworkers.workers.buy_offer.verify_offer_code_validity import verify_offer_code_validity
from camundaworkers.workers.buy_offer.verify_payment_status import verify_payment_status

TASKS = [
    ("verify-offer-code-validity", verify_offer_code_validity),
    ("rehabilitation-offer-code", rehabilitation_offer_code),
    ("send-correct-offer-code", send_correct_offer_code),
    ("send-wrong-offer-code", send_wrong_offer_code),
    ("payment-request", payment_request),
    ("send-timeout-request-payment", send_timeout_request_payment),
    ("verify-payment-status", verify_payment_status),
    ("send-wrong-payment-status", send_wrong_payment_status)
]
