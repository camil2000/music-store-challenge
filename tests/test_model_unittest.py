import unittest
from datetime import datetime
import inspect

import musicstore.model

module_members = [member[0] for member in inspect.getmembers(musicstore.model)]
transaction_defined = 'Transaction' in module_members
disc_defined = 'Disc' in module_members
music_store_defined = 'MusicStore' in module_members

if transaction_defined:
    from musicstore.model import Transaction

if disc_defined:
    from musicstore.model import Disc

if music_store_defined:
    from musicstore.model import MusicStore


class TestMusicStore(unittest.TestCase):

    def setUp(self):
        if transaction_defined:
            self.transaction = Transaction(Transaction.SELL, 5)
        if disc_defined:
            self.disc_without_transaction = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
            self.disc_with_transaction = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
            self.disc_with_transaction.transactions.append(Transaction(Transaction.SELL, 5))
            self.disc_with_songs = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
            self.disc_with_songs.add_song('Song 1')
            self.disc_with_songs.add_song('Song 2')
        if music_store_defined:
            self.empty_music_store = MusicStore()
            self.music_store_with_discs = MusicStore()
            self.music_store_with_discs.add_disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
            self.music_store_with_discs.add_disc('5678', 'Test Disc 2', 'Artist Y', 20.0, 10.0, 20)
            self.music_store_with_discs.add_disc('9012', 'Test Disc 3', 'Artist X', 20.0, 10.0, 20)

    @unittest.skipIf(not transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_has_constants(self):
        self.assertTrue(hasattr(Transaction, 'SELL'))
        self.assertEqual(Transaction.SELL, 1)
        self.assertTrue(hasattr(Transaction, 'SUPPLY'))
        self.assertEqual(Transaction.SUPPLY, 2)

    @unittest.skipIf(not transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_has_attributes(self):
        self.assertTrue(hasattr(self.transaction, 'type'))
        self.assertIsInstance(self.transaction.type, int)
        self.assertTrue(hasattr(self.transaction, 'copies'))
        self.assertIsInstance(self.transaction.copies, int)
        self.assertTrue(hasattr(self.transaction, 'date'))
        self.assertIsInstance(self.transaction.date, datetime)

    @unittest.skipIf(not transaction_defined, 'Transaction class is not defined')
    def test_class_transaction_initialization(self):
        transaction = Transaction(1, 5)
        self.assertEqual(transaction.type, 1)
        self.assertEqual(transaction.copies, 5)
        self.assertIsInstance(transaction.date, datetime)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_has_attributes(self):
        attributes = [
            ('sid', str),
            ('title', str),
            ('artist', str),
            ('sale_price', float),
            ('purchase_price', float),
            ('quantity', int),
            ('transactions', list),
            ('song_list', list),
        ]
        for attribute_name, attribute_type in attributes:
            self.assertTrue(hasattr(self.disc_without_transaction, attribute_name))
            self.assertIsInstance(getattr(self.disc_without_transaction, attribute_name), attribute_type)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_initialization(self):
        disc = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
        self.assertEqual(disc.sid, '1234')
        self.assertEqual(disc.title, 'Test Disc')
        self.assertEqual(disc.sale_price, 10.0)
        self.assertEqual(disc.purchase_price, 5.0)
        self.assertEqual(disc.quantity, 10)
        self.assertEqual(disc.transactions, [])
        self.assertEqual(disc.song_list, [])

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_has_methods(self):
        methods = [
            ('add_song', '(song: str)'),
            ('sell', '(copies: int)'),
            ('supply', '(copies: int)'),
            ('copies_sold', '()'),
            ('__str__', '()')
        ]
        for method_name, signature in methods:
            self.assertTrue(hasattr(self.disc_without_transaction, method_name))
            method = getattr(self.disc_without_transaction, method_name)
            self.assertTrue(callable(method))
            self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_add_song_method_adds_song_to_song_list(self):
        self.disc_without_transaction.add_song('Song 1')
        self.disc_without_transaction.add_song('Song 2')
        self.assertEqual(self.disc_without_transaction.song_list, ['Song 1', 'Song 2'])

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_sell_method_returns_false_and_does_not_add_transaction_when_copies_sold_exceed_quantity(self):
        self.assertFalse(self.disc_with_transaction.sell(11))
        self.assertEqual(self.disc_with_transaction.quantity, 10)
        self.assertEqual(len(self.disc_with_transaction.transactions), 1)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_sell_method_returns_true_and_adds_transaction_when_copies_sold_does_not_exceed_quantity(self):
        self.assertTrue(self.disc_with_transaction.sell(5))
        self.assertEqual(self.disc_with_transaction.quantity, 5)
        self.assertEqual(len(self.disc_with_transaction.transactions), 2)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_supply_method_increases_quantity(self):
        self.disc_with_transaction.supply(5)
        self.assertEqual(self.disc_with_transaction.quantity, 15)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_supply_method_adds_transaction(self):
        self.disc_with_transaction.supply(5)
        self.assertEqual(len(self.disc_with_transaction.transactions), 2)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_copies_sold_method_returns_total_copies_sold(self):
        self.disc_without_transaction.supply(5)
        self.disc_without_transaction.sell(1)
        self.disc_without_transaction.sell(2)
        self.disc_without_transaction.sell(3)
        self.assertEqual(self.disc_without_transaction.copies_sold(), 6)

    @unittest.skipIf(not disc_defined, 'Disc class is not defined')
    def test_class_disc_str_method_returns_string_representation(self):
        self.assertEqual(str(self.disc_with_songs), "SID: 1234\nTitle: Test Disc\nArtist: Artist X\nSong List: Song 1, Song 2")

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_has_attributes(self):
        self.assertTrue(hasattr(self.empty_music_store, 'discs'))
        self.assertIsInstance(self.empty_music_store.discs, dict)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_initialization(self):
        self.assertEqual(self.empty_music_store.discs, {})

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_has_methods(self):
        methods = [
            ('add_disc', '(sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int)'),
            ('search_by_sid', '(sid: str)'),
            ('search_by_artist', '(artist: str)'),
            ('sell_disc', '(sid: str, copies: int) -> bool'),
            ('supply_disc', '(sid: str, copies: int) -> bool'),
            ('worst_selling_disc', '()'),
        ]
        for method_name, signature in methods:
            self.assertTrue(hasattr(self.empty_music_store, method_name))
            method = getattr(self.empty_music_store, method_name)
            self.assertTrue(callable(method))
            self.assertEqual(str(inspect.signature(method)), signature)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_add_disc_method_adds_disc_to_discs(self):
        self.empty_music_store.add_disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
        self.assertIn('1234', self.empty_music_store.discs)
        self.assertIsInstance(self.empty_music_store.discs['1234'], Disc)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_does_not_add_disc_to_discs_if_sid_already_exists(self):
        self.music_store_with_discs.add_disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
        self.assertEqual(len(self.music_store_with_discs.discs), 3)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_search_by_sid_method_returns_disc(self):
        self.assertEqual(self.music_store_with_discs.search_by_sid('1234').sid, '1234')

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_search_by_sid_method_returns_none_if_sid_not_found(self):
        self.assertIsNone(self.music_store_with_discs.search_by_sid('12345'))

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_search_by_artist_method_returns_list_of_discs(self):
        self.assertEqual(len(self.music_store_with_discs.search_by_artist('Artist X')), 2)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_search_by_artist_method_returns_empty_list_if_artist_not_found(self):
        self.assertEqual(self.music_store_with_discs.search_by_artist('Artist Z'), [])

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_sell_disc_method_returns_false_if_disc_not_found(self):
        self.assertFalse(self.music_store_with_discs.sell_disc('12345', 5))

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_sell_disc_method_returns_false_if_copies_sold_exceed_quantity(self):
        self.assertFalse(self.music_store_with_discs.sell_disc('1234', 11))
        self.assertFalse(self.music_store_with_discs.sell_disc('5678', 21))

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_sell_disc_method_returns_true_if_copies_sold_does_not_exceed_quantity(self):
        self.assertTrue(self.music_store_with_discs.sell_disc('1234', 5))
        self.assertTrue(self.music_store_with_discs.sell_disc('5678', 10))

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_supply_disc_method_returns_false_if_disc_not_found(self):
        self.assertFalse(self.music_store_with_discs.supply_disc('12345', 5))

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_supply_disc_method_increases_quantity(self):
        self.music_store_with_discs.supply_disc('1234', 5)
        self.assertEqual(self.music_store_with_discs.search_by_sid('1234').quantity, 15)
        self.music_store_with_discs.supply_disc('5678', 5)
        self.assertEqual(self.music_store_with_discs.search_by_sid('5678').quantity, 25)

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_worst_selling_disc_method_returns_disc_with_least_copies_sold(self):
        self.music_store_with_discs.sell_disc('1234', 5)
        self.music_store_with_discs.sell_disc('1234', 3)
        self.music_store_with_discs.sell_disc('5678', 10)
        self.music_store_with_discs.sell_disc('9012', 9)
        self.assertEqual(self.music_store_with_discs.worst_selling_disc().sid, '1234')

    @unittest.skipIf(not music_store_defined, 'MusicStore class is not defined')
    def test_class_musicstore_worst_selling_disc_method_returns_none_if_no_discs_in_store(self):
        self.assertIsNone(self.empty_music_store.worst_selling_disc())


if __name__ == '__main__':
    unittest.main()