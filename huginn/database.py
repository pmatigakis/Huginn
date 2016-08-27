"""
The huginn.database module contains the database initialization functions
"""


from tinydb import TinyDB
from tinydb.storages import MemoryStorage


def create_database():
    """Create and initialize the the database object

    Returns the TinyDB object that will be used to store data
    """
    db = TinyDB(storage=MemoryStorage)

    db.insert(
        {
            "type": "waypoints",
            "waypoints": {}
        }
    )

    return db
