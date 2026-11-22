import sqlite3
import os
from contextlib import closing
from data import Member, Provider, Service, Transaction

def insert_transaction(transaction: Transaction, database: str = "database.db") -> int:
    if type(transaction) is not Transaction:
        raise ValueError("Expected a transaction")

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA foreign_keys = ON;")
            
            cursor.execute(""" 
                INSERT INTO transactions (
                    created_at, provided_on, provider_number,
                    member_number, service_number, fee, comment
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (transaction.created_at, transaction.provided_on,
                  int(transaction.provider_number), 
                  int(transaction.member_number),
                  int(transaction.service_number),
                  transaction.fee, transaction.comment)
            )

            transaction_id = cursor.lastrowid
                
    return transaction_id
    
def insert_service(service: Service, database: str = "database.db") -> int:
    if type(service) is not Service:
        raise ValueError("Expected a service")

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO services (
                    number, name, fee
                )
                VALUES (?, ?, ?)
            """, (int(service.number), service.name, service.fee)
            )
                
    return int(service.number)

def get_service(num: str, database: str = "database.db") -> Service | None:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM services WHERE number = ?",
                (num,)
            )

            result = cursor.fetchone()

    if result is None:
        return None
    
    ser_num = str(result[0])
    while len(ser_num) < 6:
        ser_num = '0' + ser_num

    return Service(ser_num, result[1], result[2])

def update_service(service: Service, database: str = "database.db") -> bool:
    if type(service) is not Service:
        raise ValueError("Expected a service") 

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                """ 
                UPDATE services
                SET name = ?, fee = ?
                WHERE number = ?
                """ ,
                (service.name, service.fee, int(service.number))
            )

        if cursor.rowcount == 0:
            return False

    return True 

def delete_service(num: str, database: str = "database.db") -> bool:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor() 

            cursor.execute(
                "DELETE FROM services WHERE number = ?",
                (num,)
            )

            return cursor.rowcount

def insert_provider(provider: Provider, database: str = "database.db") -> int:
    if type(provider) is not Provider:
        raise ValueError("Expected a provider")

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO providers (
                    number, name, street, city, state, zip_code
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                int(provider.number), provider.name, provider.street, 
                provider.city, provider.state, int(provider.zip_code)
            ))
                
    return int(provider.number)

def get_provider(num: str, database: str = "database.db") -> Provider | None:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM providers WHERE number = ?",
                (num,)
            )

            result = cursor.fetchone()

    if result is None:
        return None
    
    pro_num = str(result[0])
    while len(pro_num) < 9:
        pro_num = '0' + pro_num
    zip = str(result[5])
    while len(zip) < 5:
        zip = '0' + zip

    return Provider(pro_num, result[1], result[2], result[3], result[4], zip)

def update_provider(provider: Provider, database: str = "database.db") -> bool:
    if type(provider) is not Provider:
        raise ValueError("Expected a provider") 

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                """ 
                UPDATE providers
                SET name = ?, street = ?, city = ?,
                state = ?, zip_code = ?
                WHERE number = ?
                """ ,
                (provider.name, provider.street, provider.city,
                provider.state, int(provider.zip_code), int(provider.number))
            )

        if cursor.rowcount == 0:
            return False

    return True 

def delete_provider(num: str, database: str = "database.db") -> bool:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor() 

            cursor.execute(
                "DELETE FROM providers WHERE number = ?",
                (num,)
            )

            return cursor.rowcount

def insert_member(member: Member, database: str = "database.db") -> int:
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

def get_member(num: str, database: str = "database.db") -> Member | None:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM members WHERE number = ?",
                (num,)
            )

            result = cursor.fetchone()

    if result is None:
        return None
    
    mem_num = str(result[0])
    while len(mem_num) < 9:
        mem_num = '0' + mem_num
    zip = str(result[5])
    while len(zip) < 5:
        zip = '0' + zip

    return Member(mem_num, result[1], result[2], result[3], result[4],
                zip, result[6], result[7])

def update_member(member: Member, database: str = "database.db") -> bool:
    if type(member) is not Member:
        raise ValueError("Expected a Member") 

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE members
                SET name = ?, street = ?, city = ?,
                state = ?, zip_code = ?, owes = ?, 
                is_suspended = ?
                WHERE number = ?
                """,
                (member.name, member.street, member.city,
                member.state, int(member.zip_code), member.owes, 
                member.is_suspended, int(member.number))
            )

        if cursor.rowcount == 0:
            return False

    return True

def delete_member(num: str, database: str = "database.db") -> bool:
    num = int(num)

    with closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.cursor() 

            cursor.execute(
                "DELETE FROM members WHERE number = ?",
                (num,)
            )

            return cursor.rowcount

    

def delete_test_database(test_database_name: str) -> int:
    if os.path.exists(test_database_name):
        os.remove(test_database_name)
    return 0

def create_test_database(test_database_name: str) -> int:
    with closing(sqlite3.connect(test_database_name)) as conn:
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
                    fee INTEGER NOT NULL,
                    comment TEXT,
                    
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
                    fee INTEGER NOT NULL,
                    comment TEXT,

                    FOREIGN KEY (provider_number)
                        REFERENCES providers (number),
                    FOREIGN KEY (member_number) 
                        REFERENCES members (number),
                    FOREIGN KEY (service_number)
                        REFERENCES services (number)
                );

            """)
