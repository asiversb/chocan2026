import pytest
import sqlite3
from contextlib import closing
import db
from data import Member

valid_member = Member(
    "123456789",
    "John Smith",
    "1234 Street",
    "Portand",
    "OR",
    "12345"
)

invalid_member = Member(
    "thistests",
    "Int Egrity",
    "456 Street",
    "Portland",
    "OR",
    "work?"
)
def test_create_test_database():
    assert db.create_test_database() == 0

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
    assert result[0] == 123456789
    assert result[1] == "John Smith"
    assert result[2] == "1234 Street"
    assert result[3] == "Portand"
    assert result[4] == "OR"
    assert result[5] == 12345
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

def test_delete_test_database():
    assert db.delete_test_database() == 0