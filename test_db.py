import pytest
import sqlite3
from contextlib import closing
import db
from data import Member, Provider

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

def test_create_test_database():
    assert db.create_test_database("test_database.db") == 0

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