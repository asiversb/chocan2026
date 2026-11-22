from dataclasses import dataclass
from datetime import datetime      #strptime()

#Member or Provider
@dataclass
class Provider:
    number: str
    name: str
    street: str
    city: str
    state: str
    zip_code: str

    def __post_init__(self) -> None:
        if len(self.number) != 9:
            raise ValueError("Number must be a 9-digit integer.")
        if len(self.name) > 25:
            raise ValueError("Name must be a string up to 25 characters.")
        if len(self.street) > 25:
            raise ValueError("Street must be a string up to 25 characters.")
        if len(self.city) > 14:
            raise ValueError("City must be a string up to 14 characters.")
        if len(self.state) != 2:
            raise ValueError("State must be exactly 2 letters.")
        if len(self.zip_code) != 5:
            raise ValueError("Zip code must be a 5-digit integer.")

@dataclass
class Member(Provider):
    owes: int = 0 #in cents for math precision
    is_suspended: bool = False

@dataclass
class Service:
    number: str
    name: str
    fee: int #in cents for math precision

    def __post_init__(self) -> None:
        if len(self.number) != 6:
            raise ValueError("Number must be a six digit integer.")
        if len(self.name) > 20:
            raise ValueError("Name must be twenty characters or less.")
        if not (0 <= self.fee <= 99999):
            raise ValueError("Fee must be between $0.00 and $999.99.")
        

@dataclass
class Transaction:
    provided_on: str
    created_at: str
    provider_number: str
    member_number: str    #str for leading 0's?
    service_number: str     #str for leading 0's?
    fee: int #in cents for math precision 
    comment: str = ""

    def __post_init__(self) -> None:
        try:
            _ = datetime.strptime(self.provided_on, "%m-%d-%Y")
        except ValueError:
            raise ValueError("Date of service must be a valid date in MM-DD-YYYY format.")

        try:
            _ = datetime.strptime(self.created_at, "%m-%d-%Y %H:%M:%S")
        except ValueError:
            raise ValueError("Date received must be a valid timestamp in MM-DD-YYYY HH:MM:SS format.")

        if len(self.provider_number) != 9:
            raise ValueError("Provider number must be an exact 9-digit string.")
        if len(self.member_number) != 9 or not self.member_number.isdigit():
            raise ValueError("Member number must be an exact 9-digit string.")
        if len(self.service_number) != 6 or not self.service_number.isdigit():
            raise ValueError("Service code must be an exact 6-digit string.")
        if not (0 <= self.fee <= 99999):
            raise ValueError("Fee must be between $0.00 and $999.99.")
        if len(self.comment) > 100:
            raise ValueError("Comment must be below 100 characters.")


