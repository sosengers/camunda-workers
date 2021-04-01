class PurchaseError:
    def __init__(self, message: str):
        self.message = message

    def to_dict(self):
        error = {}
        error['message'] = self.message
        return error