class PurchaseProcessInformation:
    def __init__(self, message: str, communication_code: str, is_error: bool = False):
        self.communication_code = communication_code
        self.message = message
        self.is_error = is_error

    def to_dict(self):
        message = {
            "message": self.message,
            "communication_code": self.communication_code,
            "is_error": self.is_error
        }
        return message