from .save_last_minute_offers import save_last_minute_offers
from .retrieve_user_interests import retrieve_user_interests

TASKS = [
    ("save-last-minute-offers", save_last_minute_offers),
    ("retrieve-user-interests", retrieve_user_interests)
]
