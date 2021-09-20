from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import shortuuid


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def add_url(url, num_uses):
    """
    Returns:
        bool: did the function execute as expected
        str: corresponding id
    """
    try:
        uuid = shortuuid.uuid()
        data = {"_id": uuid, "url": url, "num_uses": num_uses}
        db.urls.insert_one(data)
        return True, data
    except Exception as e:
        return False, {"message": str(e)}


def get_document_by_id(id):
    """
    Returns:
        bool: did the function execute as expected
        dict: corresponding dictionary
    """
    try:
        data = db.urls.find_one({"_id": id})
        return True, data
    except Exception as e:
        return False, {"message": str(e)}


def decrement_document_by_id(id):
    """
    Returns:
        bool: did the function execute as expected
        dict: corresponding dictionary
    """
    try:
        filter = {"_id": id}
        new_values = {"$inc": { "num_uses": -1 }}
        db.urls.update_one(filter, new_values)
        return True, {}
    except Exception as e:
        return False, {"message": str(e)}


def get_document_by_url(url):
    """
    Returns:
        bool: did the function execute as expected
        dict: corresponding dictionary
    """
    try:
        data = db.urls.find_one({"url": url})
        return True, data
    except Exception as e:
        return False, {"message": str(e)}
