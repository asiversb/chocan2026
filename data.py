from dataclasses import dataclass
from datetime import datetime      #strptime()

#Member or Provider
@dataclass
class User:
    name: str
    street: str
    city: str
    state: str
    zip_code: int

    def __post_init__(self) -> None:
        if len(self.name) > 25:
            raise ValueError("Name must be a string up to 25 characters.")
        if len(self.street) > 25:
            raise ValueError("Street must be a string up to 25 characters.")
        if len(self.city) > 14:
            raise ValueError("City must be a string up to 14 characters.")
        if len(self.state) != 2:
            raise ValueError("State must be exactly 2 letters.")
        if not (10000 <= self.zip_code <= 99999):
            raise ValueError("Zip code must be a 5-digit integer.")

@dataclass
class Transactions:
    date_of_service: str
    date_received: str
    member_name: str
    member_number: str    #str for leading 0's?
    service_code: str     #str for leading 0's?
    fee: float

    def __post_init__(self) -> None:
        try:
            _ = datetime.strptime(self.date_of_service, "%m-%d-%Y")
        except ValueError:
            raise ValueError("Date of service must be a valid date in MM-DD-YYYY format.")

        try:
            _ = datetime.strptime(self.date_received, "%m-%d-%Y %H:%M:%S")
        except ValueError:
            raise ValueError("Date received must be a valid timestamp in MM-DD-YYYY HH:MM:SS format.")

        if len(self.member_name) > 25:
            raise ValueError("Member name must be a string up to 25 characters.")
        if len(self.member_number) != 9 or not self.member_number.isdigit():
            raise ValueError("Member number must be an exact 9-digit string.")
        if len(self.service_code) != 6 or not self.service_code.isdigit():
            raise ValueError("Service code must be an exact 6-digit string.")
        if not (0.0 <= self.fee <= 999.99):
            raise ValueError("Fee must be between $0.00 and $999.99.")


