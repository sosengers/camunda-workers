class Address:
    def __init__(self, street: str, number: str, city: str, zip_code: str, country: str):
        self.street = street
        self.number = number
        self.city = city
        self.zip_code = zip_code
        self.country = country
    
    @staticmethod
    def from_dict(data: dict):
        return Address(
            street=data.get('street'),
            number=data.get('number'),
            city=data.get('city'),
            zip_code=data.get('zip_code'),
            country=data.get('country')
        )

        
    def __key(self):
        return (self.street, self.number, self.city, self.zip_code, self.country)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Address):
            return self.__key() == other.__key()
        return NotImplemented