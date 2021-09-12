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


def add_url(url):
    uuid = shortuuid.uuid()
    data = {'_id': uuid, 'url': url}
    return db.urls.insert_one(data)


def get_url(id):
    return db.urls.find_one({'_id': id})
