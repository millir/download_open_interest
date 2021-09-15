

class OpenInterest:
    def __init__(self) -> None:
        self.contract = None
        self.open_interest = None
    
    def add_contract(self, contract: str):
        self.contract = contract

    def add_open_interest(self, open_interest: int):
        self.open_interest = open_interest

    def validate_values_are_set(self):
        if self.contract and self.open_interest:
            return True
        else:
            return False
