import sqlite3
import os
from contextlib import closing
from data import Member


def create_member(member : Member, database : str = "database.db") -> int:
    if type(member) is not Member:
        raise ValueError("Expected a Member")

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO members (
                    number, name, street, city, state, 
                    zip_code, owes, is_suspended
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(member.number), member.name, member.street, member.city,
                member.state, int(member.zip_code), member.owes, 
                member.is_suspended
            ))
                
    return int(member.number)


def delete_test_database() -> int:
    if os.path.exists("test_database.db"):
        os.remove("test_database.db")
    return 0

def create_test_database() -> int:
    with closing(sqlite3.connect("test_database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS members (
                    number INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL, 
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code INTEGER NOT NULL,
                    owes INTEGER NOT NULL DEFAULT 0,
                    is_suspended INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS providers (
                    number INTEGER PRIMARY KEY,
                    name TEXT NOT NULL, 
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS services (
                    number INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL,
                    fee INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS transactions (  
                    id INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    provided_on TEXT NOT NULL,
                    provider_number INTEGER NOT NULL,
                    member_number INTEGER NOT NULL,
                    service_number INTEGER NOT NULL, 
                    FOREIGN KEY (provider_number)
                        REFERENCES providers (number),
                    FOREIGN KEY (member_number) 
                        REFERENCES members (number),
                    FOREIGN KEY (service_number)
                        REFERENCES services (number)
                );

            """)
    return 0

def create_database():
    with closing(sqlite3.connect("database.db")) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS members (
                    number INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL, 
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code INTEGER NOT NULL,
                    owes INTEGER NOT NULL DEFAULT 0,
                    is_suspended INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS providers (
                    number INTEGER PRIMARY KEY,
                    name TEXT NOT NULL, 
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS services (
                    number INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL,
                    fee INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS transactions (  
                    id INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    provided_on TEXT NOT NULL,
                    provider_number INTEGER NOT NULL,
                    member_number INTEGER NOT NULL,
                    service_number INTEGER NOT NULL, 
                    FOREIGN KEY (provider_number)
                        REFERENCES providers (number),
                    FOREIGN KEY (member_number) 
                        REFERENCES members (number),
                    FOREIGN KEY (service_number)
                        REFERENCES services (number)
                );

            """)
