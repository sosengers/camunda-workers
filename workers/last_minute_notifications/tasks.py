from .save_last_minute_offers import save_last_minute_offers
from .retrieve_user_interests import retrieve_user_interests
from .check_offers_presence import check_offers_presence

TASKS = [
    ("save-last-minute-offers", save_last_minute_offers),
    ("retrieve-user-interests", retrieve_user_interests),
    ("check-offers-presence", check_offers_presence)
]
