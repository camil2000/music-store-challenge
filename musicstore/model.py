from datetime import datetime

# TODO: Add code here

class Transaction:

    SELL = 1
    SUPPLY = 2

    def __init__(self, type: int, copies: int):
        self.type = type
        self.copies = copies
        self.date = datetime.now()
