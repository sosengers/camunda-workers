class PurchaseProcessInformation:
    def __init__(self, message: str, is_error: bool = False):
        self.message = message
        self.is_error = is_error

    def to_dict(self):
        error = {}
        error['message'] = self.message
        error['is_error'] = self.is_error
        return error