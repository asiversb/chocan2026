import sqlite3
from contextlib import closing

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
                    start TEXT NOT NULL,
                    zip_code INTEGER NOT NULL,
                    owes INTEGER NOT NULL DEFAULT 0,
                    is_suspended INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS providers (
                    number INTEGER PRIMARY KEY,
                    name TEXT NOT NULL, 
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    start TEXT NOT NULL,
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
