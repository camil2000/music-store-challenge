from datetime import datetime

# TODO: Add code here

class Transaction:

    SELL = 1
    SUPPLY = 2

    def __init__(self, type: int, copies: int):
        self.type = type
        self.copies = copies
        self.date = datetime.now()


class Disc:

    def __init__(self, sid: str, title: str, artist: str,
                 sale_price: float, purchase_price: float, quantity: int):

        self.sid = sid
        self.title = title
        self.artist = artist
        self.sale_price = sale_price
        self.purchase_price = purchase_price
        self.quantity = quantity

