"""Database modules."""
from bson.objectid import ObjectId
from database_manager import DatabaseManager
import local_settings


# Database instance
database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)

# Collection instance
collection = database_manager.create_collection(model="contacts")


class Contact:
    """Contact model."""
    def __init__(self, first_name, last_name, number, address):
        """Constructor."""
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.address = address

    def get_contact(self):
        """Return contact.

        :return: contact as dict.
        """
        return {
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Number': self.number,
            'Address': self.address,
        }

    @classmethod
    def create(cls, first_name, last_name, number, address):
        """Create contact and insert it to the database."""
        contact_instance = cls(first_name, last_name, number, address)
        contact = contact_instance.get_contact()
        collection.insert_one(contact)

    @classmethod
    def delete(cls, contact):
        """Delete contact from the database."""
        collection.delete_one(contact)

    @classmethod
    def delete_by_id(cls, contact_id):
        """Delete contact from the database by id."""
        collection.find_one_and_delete({"_id": ObjectId(contact_id)})
        print(contact_id)


def initialize_database():
    """Initialize database.

    Create tables if they don't exist and fill with initial values.
    if you don't want to initialize the database:
    set sample_settings.first_init to False.
    """
    try:
        # Warning
        print("start initializing database")
        # # you can uncomment these statements For more caution.
        # print("do you want to continue? [y/n]")
        # if input().lower() not in ['y', 'yes']:
        #     exit()

        # Create table
        with open("init_data.txt", "r") as init:
            for line in init:
                contact = line.split(",")
                print(line)
                Contact.create(
                    first_name=contact[0],
                    last_name=contact[1],
                    number=contact[2],
                    address=contact[3],
                )
    except Exception as e:
        print("Error", e)


def get_contacts():
    """Get all contacts.

    :return: list[dict] of all contacts
    """
    try:
        contacts = collection.find()
        for contact in contacts:
            yield contact
    except Exception as e:
        print("Error", e)


def add_contact(first_name, last_name, number, address=None):
    """Add contact to database.

    :param first_name: first name
    :param last_name: last name
    :param number: contact number
    :param address: contact address
    """
    try:
        Contact.create(
            first_name=first_name,
            last_name=last_name,
            number=number,
            address=address,
        )
    except Exception as e:
        print("Error", e)


def delete_contact(id_row: int):
    """Delete contact by id.

    :param id_row: contact id
    """
    try:
        Contact.delete_by_id(id_row)
    except Exception as e:
        print("Error", e)


def search_contact(search_term: str):
    """Search contact in database.

    :param search_term: search term
    :return: list[dict] of retrieved contacts
    """
    try:
        retrieved_data = collection.aggregate(
            [
                {
                    "$match":
                        {
                            "$or":
                            [
                                {"First Name": {"$regex": f"{search_term}"}},
                                {"Last Name": {"$regex": f"{search_term}"}},
                                {"Number": {"$regex": f"{search_term}"}},
                                {"Address": {"$regex": f"{search_term}"}},
                            ]

                        }
                },
            ]
        )
        for contact in retrieved_data:
            yield contact
    except Exception as e:
        print("Error", e)


# initialize database
# # Attention: after first start set local_settings.first_init to False
if local_settings.first_init:
    initialize_database()
