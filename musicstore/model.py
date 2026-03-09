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

        self.transactions: list[Transaction] = []
        self.song_list: list[str] = []

    def add_song(self, song: str):
        self.song_list.append(song)

    def sell(self, copies: int):

        if copies > self.quantity:
            return False

        self.quantity -= copies
        self.transactions.append(Transaction(Transaction.SELL, copies))

        return True

    def supply(self, copies: int):

        self.quantity += copies
        self.transactions.append(Transaction(Transaction.SUPPLY, copies))

    def copies_sold(self):

        total = 0

        for transaction in self.transactions:
            if transaction.type == Transaction.SELL:
                total += transaction.copies

        return total

    def __str__(self):

        songs = ", ".join(self.song_list)

        return f"SID: {self.sid}\nTitle: {self.title}\nArtist: {self.artist}\nSong List: {songs}"

class MusicStore:

    def __init__(self):
        self.discs: dict[str, Disc] = {}

    def add_disc(self, sid: str, title: str, artist: str,
                 sale_price: float, purchase_price: float, quantity: int):

        if sid not in self.discs:
            disc = Disc(sid, title, artist, sale_price, purchase_price, quantity)
            self.discs[sid] = disc

    def search_by_sid(self, sid: str):

        if sid in self.discs:
            return self.discs[sid]

        return None

    def search_by_artist(self, artist: str):

        result = []

        for disc in self.discs.values():
            if disc.artist == artist:
                result.append(disc)

        return result

    def sell_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        return disc.sell(copies)

    def supply_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        disc.supply(copies)
        return True

    def worst_selling_disc(self):

        if len(self.discs) == 0:
            return None

        worst = None

        for disc in self.discs.values():
            if worst is None or disc.copies_sold() < worst.copies_sold():
                worst = disc

        return worst
