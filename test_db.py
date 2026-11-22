import pytest
import sqlite3
from contextlib import closing
import db
from data import Member, Provider, Service, Transaction

valid_member = Member(
    "003456789",
    "John Smith",
    "1234 Street",
    "Portand",
    "OR",
    "00345"
)

invalid_member = Member(
    "thistests",
    "Int Egrity",
    "456 Street",
    "Portland",
    "OR",
    "work?"
)

valid_provider = Provider(
    "000000789",
    "Shane Man",
    "123 Lane",
    "Portland",
    "OR",
    "00001"
)

invalid_provider = Provider(
    "00.45!000",
    "Strange",
    "456 Ave",
    "Portland",
    "OR",
    "NOT E"
)

valid_service = Service(
    "000456",
    "Massage",
    500
)

invalid_service = Service(
    "testin",
    "the function",
    400
)

valid_transaction = Transaction(
    "11-21-2026",
    "11-21-2026 04:06:00",
    valid_provider.number,
    valid_member.number,
    valid_service.number,
    valid_service.fee,
    "Hello there!"
)

invalid_transaction = Transaction(
    "11-21-2026",
    "11-21-2026 04:06:00",
    valid_provider.number,
    "678452123",
    valid_service.number,
    valid_service.fee,
    "Hello there!" 
)

def test_create_test_database():
    assert db.create_test_database("test_database.db") == 0

def test_insert_transaction_valid():
    db.insert_member(valid_member, "test_database.db")
    db.insert_provider(valid_provider, "test_database.db")
    db.insert_service(valid_service, "test_database.db")

    transaction_id = db.insert_transaction(valid_transaction, "test_database.db")

    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            result = cursor.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,)
            ).fetchone()

    assert result is not None
    assert result[0] == transaction_id
    assert result[2] == "11-21-2026"
    assert result[1] == "11-21-2026 04:06:00"
    assert result[3] == int(valid_provider.number)
    assert result[4] == int(valid_member.number)
    assert result[5] == int(valid_service.number)
    assert result[6] == valid_service.fee
    assert result[7] == "Hello there!"

def test_insert_transaction_duplicate():
    transaction_id = db.insert_transaction(valid_transaction, "test_database.db")

    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            result = cursor.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,)
            ).fetchone()

    assert result is not None
    assert result[0] == transaction_id
    assert result[2] == "11-21-2026"
    assert result[1] == "11-21-2026 04:06:00"
    assert result[3] == int(valid_provider.number)
    assert result[4] == int(valid_member.number)
    assert result[5] == int(valid_service.number)
    assert result[6] == valid_service.fee
    assert result[7] == "Hello there!"
    
def test_insert_transaction_invalid():
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_transaction(invalid_transaction, "test_database.db")

def test_insert_transaction_wrong_type():
    with pytest.raises(ValueError):
        db.insert_transaction("test", "test_database.db")

def test_insert_transaction_delete():
    db.delete_member(valid_member.number, "test_database.db")
    db.delete_provider(valid_provider.number, "test_database.db")
    db.delete_service(valid_service.number, "test_database.db")

def test_insert_service_valid():
    service_number = db.insert_service(valid_service, "test_database.db")

    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            result = cursor.execute(
                "SELECT * FROM services WHERE number = ?",
                (service_number,)
            ).fetchone()

    assert result is not None
    assert result[0] == 456
    assert result[1] == "Massage"
    assert result[2] == 500

def test_insert_service_duplicate():
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_service(valid_service, "test_database.db")

def test_insert_service_invalid():
    with pytest.raises(ValueError):
        db.insert_service(invalid_service, "test_database.db")

def test_insert_service_wrong_type():
    with pytest.raises(ValueError):
        db.insert_service("test", "test_database.db")

def test_get_service_doesnt_exist():
    assert None == db.get_service("987654", "test_database.db")

def test_get_service_valid():
    assert valid_service == db.get_service(valid_service.number, "test_database.db")

def test_get_service_invalid():
    with pytest.raises(ValueError):
        db.get_service(invalid_service.number, "test_database.db")

def test_update_service_valid():
    valid_service.name = "Jane Smith"
    assert True == db.update_service(valid_service, "test_database.db")
    assert db.get_service(valid_service.number, "test_database.db").name == "Jane Smith"

def test_update_service_invalid():
    with pytest.raises(ValueError):
        db.update_service(invalid_service, "test_database.db")

def test_update_service_wrong_type():
    with pytest.raises(ValueError):
        db.update_service("test", "test_database.db")

def test_update_service_doesnt_exist():
    de = Service("444444","Name", 99999)
    assert False == db.update_service(de, "test_database.db")

def test_delete_service_valid():
    assert True == db.delete_service(valid_service.number, "test_database.db")

def test_delete_service_doesnt_exist():
    assert False == db.delete_service(valid_service.number, "test_database.db")

def test_delete_service_invalid():
    with pytest.raises(ValueError):
        db.delete_service(invalid_service.number, "test_database.db")
        
def test_insert_provider_valid():
    provider_number = db.insert_provider(valid_provider, "test_database.db")

    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            result = cursor.execute(
                "SELECT * FROM providers WHERE number = ?",
                (provider_number,)
            ).fetchone()

    assert result is not None
    assert result[0] == 789
    assert result[1] == "Shane Man"
    assert result[2] == "123 Lane"
    assert result[3] == "Portland"
    assert result[4] == "OR"
    assert result[5] == 1

def test_insert_provider_duplicate():
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_provider(valid_provider, "test_database.db")

def test_insert_provider_invalid():
    with pytest.raises(ValueError):
        db.insert_provider(invalid_provider, "test_database.db")

def test_insert_provider_wrong_type():
    with pytest.raises(ValueError):
        db.insert_provider("test", "test_database.db")

def test_get_provider_valid():
    assert valid_provider == db.get_provider(valid_provider.number, "test_database.db")

def test_get_provider_invalid():
    with pytest.raises(ValueError):
        db.get_provider(invalid_provider.number, "test_database.db")

def test_get_provider_doesnt_exist():
    assert None == db.get_provider("987654321", "test_database.db")

def test_update_provider_valid():
    valid_provider.name = "Jane Smith"
    assert True == db.update_provider(valid_provider, "test_database.db")
    assert db.get_provider(valid_provider.number, "test_database.db").name == "Jane Smith"

def test_update_provider_invalid():
    with pytest.raises(ValueError):
        db.update_provider(invalid_provider, "test_database.db")

def test_update_provider_wrong_type():
    with pytest.raises(ValueError):
        db.update_provider("test", "test_database.db")

def test_update_provider_doesnt_exist():
    de = Provider("444444444","e", "e", "e", "EE", "55555")
    assert False == db.update_provider(de, "test_database.db")

def test_delete_provider_valid():
    assert True == db.delete_provider(valid_provider.number, "test_database.db")

def test_delete_provider_doesnt_exist():
    assert False == db.delete_provider(valid_provider.number, "test_database.db")

def test_delete_provider_invalid():
    with pytest.raises(ValueError):
        db.delete_provider(invalid_provider.number, "test_database.db")

def test_insert_member_valid():
    member_number = db.insert_member(valid_member, "test_database.db")

    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            result = cursor.execute(
                "SELECT * FROM members WHERE number = ?",
                (member_number,)
            ).fetchone()

    assert result is not None
    assert result[0] == 3456789
    assert result[1] == "John Smith"
    assert result[2] == "1234 Street"
    assert result[3] == "Portand"
    assert result[4] == "OR"
    assert result[5] == 345
    assert result[6] == 0
    assert result[7] == 0

def test_insert_member_duplicate():
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_member(valid_member, "test_database.db")

def test_insert_member_invalid():
    with pytest.raises(ValueError):
        db.insert_member(invalid_member, "test_database.db")

def test_insert_member_wrong_type():
    with pytest.raises(ValueError):
        db.insert_member("test", "test_database.db")

def test_get_member_valid():
    assert valid_member == db.get_member(valid_member.number, "test_database.db")

def test_get_member_invalid():
    with pytest.raises(ValueError):
        db.get_member(invalid_member.number, "test_database.db")

def test_get_member_doesnt_exist():
    assert None == db.get_member("987654321", "test_database.db")

def test_update_member_valid():
    valid_member.name = "Jane Smith"
    assert True == db.update_member(valid_member, "test_database.db")
    assert db.get_member(valid_member.number, "test_database.db").name == "Jane Smith"

def test_update_member_invalid():
    with pytest.raises(ValueError):
        db.update_member(invalid_member, "test_database.db")

def test_update_member_wrong_type():
    with pytest.raises(ValueError):
        db.update_member("test", "test_database.db")

def test_update_member_doesnt_exist():
    de = Member("444444444","e", "e", "e", "EE", "55555")
    assert False == db.update_member(de, "test_database.db")

def test_delete_member_valid():
    assert True == db.delete_member(valid_member.number, "test_database.db")

def test_delete_member_doesnt_exist():
    assert False == db.delete_member(valid_member.number, "test_database.db")

def test_delete_member_invalid():
    with pytest.raises(ValueError):
        db.delete_member(invalid_member.number, "test_database.db")
        
def test_delete_test_database():
    assert db.delete_test_database("test_database.db") == 0