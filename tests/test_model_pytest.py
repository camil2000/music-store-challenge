from datetime import datetime
import inspect

import pytest

import musicstore.model 


module_members = [member[0] for member in inspect.getmembers(musicstore.model)]
trasaction_defined = 'Transaction' in module_members
disc_defined = 'Disc' in module_members
music_store_defined = 'MusicStore' in module_members


if trasaction_defined:
    from musicstore.model import Transaction

if disc_defined:
    from musicstore.model import Disc

if music_store_defined:
    from musicstore.model import MusicStore

@pytest.fixture
def transaction():
    return Transaction(Transaction.SELL, 5)

    
@pytest.fixture
def disc_without_transaction():
    return Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)


@pytest.fixture
def disc_with_transaction():
    disc = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
    disc.transactions.append(Transaction(Transaction.SELL, 5))
    return disc

@pytest.fixture
def empty_music_store():
    return MusicStore()

@pytest.fixture
def music_store_with_discs():
    music_store = MusicStore()
    music_store.add_disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
    music_store.add_disc('5678', 'Test Disc 2', 'Artist Y', 20.0, 10.0, 20)
    music_store.add_disc('9012', 'Test Disc 3', 'Artist X', 20.0, 10.0, 20)
    return music_store

@pytest.fixture
def disc_with_songs():
    disc = Disc('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10)
    disc.add_song('Song 1')
    disc.add_song('Song 2')
    return disc


# Test the Transaction class
@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('constant_name, constant_value', [
    ('SELL', 1),
    ('SUPPLY', 2)
])
def test_class_transaction_has_constants(constant_name, constant_value):
    assert hasattr(Transaction, constant_name)
    assert getattr(Transaction, constant_name) == constant_value

@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('type', int),
    ('copies', int),
    ('date', datetime)
])
def test_class_transaction_has_attributes(transaction, attribute_name, attribute_type):
    assert hasattr(transaction, attribute_name)
    assert isinstance(getattr(transaction, attribute_name), attribute_type)

@pytest.mark.skipif(not trasaction_defined, reason='Transaction class is not defined')
@pytest.mark.parametrize('transaction_type, copies', [
    (1, 5),
    (2, 10)
])   
def test_class_transaction_initilization(transaction_type, copies):
    transaction = Transaction(transaction_type, copies)
    assert transaction.type == transaction_type
    assert transaction.copies == copies
    assert isinstance(transaction.date, datetime)
    


# Test the Disc class
@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('sid', str),
    ('title', str),
    ('artist', str),
    ('sale_price', float),
    ('purchase_price', float),
    ('quantity', int),
    ('transactions', list),
    ('song_list', list),
])
def test_class_disc_has_attributes(disc_without_transaction, attribute_name, attribute_type):
    assert hasattr(disc_without_transaction, attribute_name)
    assert isinstance(getattr(disc_without_transaction, attribute_name), attribute_type)


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
@pytest.mark.parametrize('sid, title, artist, sale_price, purchase_price, quantity', [
    ('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10),
    ('5678', 'Test Disc 2', 'Artist Y', 20.0, 10.0, 20),
    ('91011', 'Test Disc 3', 'Artist Z', 30.0, 15.0, 30),
    ('121314', 'Test Disc 4', 'Artist W', 40.0, 20.0, 40)
])
def test_class_disc_initilization(sid, title, artist, sale_price, purchase_price, quantity):
    disc = Disc(sid, title, artist, sale_price, purchase_price, quantity)
    assert disc.sid == sid
    assert disc.title == title
    assert disc.sale_price == sale_price
    assert disc.purchase_price == purchase_price
    assert disc.quantity == quantity
    assert disc.transactions == []
    assert disc.song_list == []


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
@pytest.mark.parametrize('method_name, signature', [
    ('add_song', '(song: str)'),
    ('sell', '(copies: int) -> bool'),
    ('supply', '(copies: int)'),
    ('copies_sold', '() -> int'),
    ('__str__', '() -> str')
])
def test_class_disc_has_methods(disc_without_transaction, method_name, signature):
    assert hasattr(disc_without_transaction, method_name)
    method = getattr(disc_without_transaction, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_add_song_method_adds_song_to_song_list(disc_without_transaction):
    disc_without_transaction.add_song('Song 1')
    disc_without_transaction.add_song('Song 2')
    assert disc_without_transaction.song_list == ['Song 1', 'Song 2']

@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_sell_method_returns_false_and_does_not_add_transaction_when_copies_sold_exceed_quantity(disc_with_transaction):
    assert not disc_with_transaction.sell(11)
    assert disc_with_transaction.quantity == 10
    assert len(disc_with_transaction.transactions) == 1

@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_sell_method_returns_true_and_adds_transaction_when_copies_sold_does_not_exceed_quantity(disc_with_transaction):
    assert disc_with_transaction.sell(5)
    assert disc_with_transaction.quantity == 5
    assert len(disc_with_transaction.transactions) == 2

@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_supply_method_increases_quantity(disc_with_transaction):
    disc_with_transaction.supply(5)
    assert disc_with_transaction.quantity == 15


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_supply_method_adds_transaction(disc_with_transaction):
    disc_with_transaction.supply(5)
    assert len(disc_with_transaction.transactions) == 2


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
@pytest.mark.parametrize('copies_supplied, copies_sold', [
    (5, (1, 2, 3)),
    (8, (2, 1)),
    (1, (1,))
])
def test_class_disc_copies_sold_method_returns_total_copies_sold(disc_without_transaction, copies_supplied, copies_sold):
    disc_without_transaction.supply(copies_supplied)
    for copies in copies_sold:
        disc_without_transaction.sell(copies)
    assert disc_without_transaction.copies_sold() == sum(copies_sold)


@pytest.mark.skipif(not disc_defined, reason='Disc class is not defined')
def test_class_disc_str_method_returns_string_representation(disc_with_songs):
    assert str(disc_with_songs) == "SID: 1234\n" \
                                    "Title: Test Disc\n" \
                                    "Artist: Artist X\n" \
                                    "Song List: Song 1, Song 2"


# Test the MusicStore class
@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('attribute_name, attribute_type', [
    ('discs', dict)
])
def test_class_musicstore_has_attributes(empty_music_store, attribute_name, attribute_type):
    assert hasattr(empty_music_store, attribute_name)
    assert isinstance(getattr(empty_music_store, attribute_name), attribute_type)

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_initilization(empty_music_store):
    assert empty_music_store.discs == {}


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('method_name, signature', [
    ('add_disc', '(sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int)'),
    ('search_by_sid', '(sid: str) -> musicstore.model.Disc | None'),
    ('search_by_artist', '(artist: str) -> list[musicstore.model.Disc]'),
    ('sell_disc', '(sid: str, copies: int) -> bool'),
    ('supply_disc', '(sid: str, copies: int) -> bool'),
    ('worst_selling_disc', '() -> musicstore.model.Disc | None'),
])
def test_class_musicstore_has_methods(empty_music_store, method_name, signature):
    assert hasattr(empty_music_store, method_name)
    method = getattr(empty_music_store, method_name)
    assert callable(method)
    assert str(inspect.signature(method)) == signature
    

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid, title, artist, sale_price, purchase_price, quantity', [
    ('1234', 'Test Disc', 'Artist X',10.0, 5.0, 10),
    ('5678', 'Test Disc 2', 'Artist Y', 20.0, 10.0, 20),
    ('91011', 'Test Disc 3', 'Artist Z', 30.0, 15.0, 30),
])
def test_class_musicstore_add_disc_method_adds_disc_to_discs(empty_music_store, sid, title, artist, sale_price, purchase_price, quantity):
    empty_music_store.add_disc(sid, title, artist, sale_price, purchase_price, quantity)
    assert sid in empty_music_store.discs
    assert isinstance(empty_music_store.discs[sid], Disc)


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid, title, artist, sale_price, purchase_price, quantity', [
    ('1234', 'Test Disc', 'Artist X', 10.0, 5.0, 10),
    ('5678', 'Test Disc 2', 'Artist Y', 20.0, 10.0, 20),
])
def test_class_musicstore_does_not_add_disc_to_discs_if_sid_already_exists(music_store_with_discs, sid, title, artist, sale_price, purchase_price, quantity):
    music_store_with_discs.add_disc(sid, title, artist, sale_price, purchase_price, quantity)
    assert len(music_store_with_discs.discs) == 3


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid', [
    '1234',
    '5678'
])
def test_class_musicstore_search_by_sid_method_returns_disc(music_store_with_discs, sid):
    assert music_store_with_discs.search_by_sid(sid).sid == sid

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_search_by_sid_method_returns_none_if_sid_not_found(music_store_with_discs):
    assert music_store_with_discs.search_by_sid('12345') is None

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_search_by_artist_method_returns_list_of_discs(music_store_with_discs):
    assert len(music_store_with_discs.search_by_artist('Artist X')) == 2

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_search_by_artist_method_returns_empty_list_if_artist_not_found(music_store_with_discs):
    assert music_store_with_discs.search_by_artist('Artist Z') == []

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_sell_disc_method_returns_false_if_disc_not_found(music_store_with_discs):
    assert not music_store_with_discs.sell_disc('12345', 5)

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid, quantity', [
    ('1234', 11),
    ('5678', 21)
])
def test_class_musicstore_sell_disc_method_returns_false_if_copies_sold_exceed_quantity(music_store_with_discs, sid, quantity):
    assert not music_store_with_discs.sell_disc(sid, quantity)

@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid, quantity', [
    ('1234', 5),
    ('5678', 10)
])
def test_class_musicstore_sell_disc_method_returns_true_if_copies_sold_does_not_exceed_quantity(music_store_with_discs, sid, quantity):
    assert music_store_with_discs.sell_disc(sid, quantity)


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_supply_disc_method_returns_false_if_disc_not_found(music_store_with_discs):
    assert not music_store_with_discs.supply_disc('12345', 5)


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
@pytest.mark.parametrize('sid, total', [
    ('1234', 15),
    ('5678', 25)
])
def test_class_musicstore_supply_disc_method_increases_quantity(music_store_with_discs, sid, total):
    music_store_with_discs.supply_disc(sid, 5)
    assert music_store_with_discs.search_by_sid(sid).quantity == total


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_worst_selling_disc_method_returns_disc_with_least_copies_sold(music_store_with_discs):
    music_store_with_discs.sell_disc('1234', 5)
    music_store_with_discs.sell_disc('1234', 3)
    music_store_with_discs.sell_disc('5678', 10)
    music_store_with_discs.sell_disc('9012', 9)
    assert music_store_with_discs.worst_selling_disc().sid == '1234'


@pytest.mark.skipif(not music_store_defined, reason='MusicStore class is not defined')
def test_class_musicstore_worst_selling_book_method_returns_none_if_no_discs_in_store(empty_music_store):
    assert empty_music_store.worst_selling_disc() is None
    