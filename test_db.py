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

def test_create_member_valid(valid_member):
    member_number = db.create_member(valid_member)

    with closing(sqlite3.connect("database.db")) as conn:
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



def test_create_member_duplicate(valid_member):
    with pytest.raises(db.DuplicateError):
        db.create_member(valid_member)

def test_create_member_invalid(invalid_member):
    with pytest.raises(ValueError):
        db.create_member(invalid_member)

def test_create_member_wrong_type():
    with pytest.raises(ValueError):
        db.create_member("test")