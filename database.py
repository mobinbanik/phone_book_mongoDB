"""Q.
"""
from database_manager import DatabaseManager
import local_settings

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


class Contact:
    def __init__(self, first_name, last_name, number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.address = address

    def get_contact(self):
        return {
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Number': self.number,
            'Address': self.address,
        }

    @classmethod
    def create(cls, first_name, last_name, number, address):
        contact_instance = cls(first_name, last_name, number, address)
        contact = contact_instance.get_contact()
        database_manager.mongo_db.


def initialize_database():
    try:
        database_manager.create_tables(models=[Contact])
        with open("init_data.txt", "r") as init:
            for line in init:
                contact = line.split(",")
                Contact.create(
                    first_name=contact[0],
                    last_name=contact[1],
                    number=contact[2],
                    address=contact[3],
                )
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.mongo_db:
            database_manager.close_connection()
            print("Database connection is closed")


def get_contacts():
    try:
        contacts = Contact.select()
        for contact in contacts:
            yield {
                "First Name": contact.first_name,
                "Last Name": contact.last_name,
                "Number": contact.number,
                "Address": contact.address,
                "Id": str(contact.get_id()),
            }
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")


def add_contact(first_name, last_name, number, address=None):
    try:
        Contact.create(
            first_name=first_name,
            last_name=last_name,
            number=number,
            address=address,
        )
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.mongo_db:
            database_manager.close_connection()
            print("Database connection is closed")


def delete_contact(id_row: int):
    try:
        Contact.delete_by_id(id_row)
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.mongo_db:
            database_manager.close_connection()
            print("Database connection is closed")


def search_contact(search_term: str):
    try:
        retrieved_data = Contact.select().where(
            (Contact.first_name.contains(search_term))
            | (Contact.last_name.contains(search_term))
            | (Contact.number.contains(search_term))
            | (Contact.address.contains(search_term))
        )
        for contact in retrieved_data:
            yield {
                "First Name": contact.first_name,
                "Last Name": contact.last_name,
                "Number": contact.number,
                "Address": contact.address,
                "Id": str(contact.get_id()),
            }
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.mongo_db:
            database_manager.close_connection()
            print("Database connection is closed")


# initialize database
# # Attention: after first start set local_settings.first_init to False
if local_settings.first_init:
    initialize_database()
