import pymongo
import click
from flask import g, current_app
from flask.cli import with_appcontext

def get_db():
    mongocon = current_app.config['MONGO_URI']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]


def get_ponds():
    collection = get_collection('pond')
    return collection.find()

def insert_pond(data):
    collection = get_collection('pond')
    row = collection.insert_one(data)
    return row

def get_pond(filter = {}):
    collection = get_collection('pond')
    return collection.find_one(filter)

def update_pond(filter, newvalues):
    collection = get_collection('pond')
    return collection.update_one(filter, newvalues)
    

def close_db(e=None):
    db = g.pop(current_app.config['DATABASE'], None)
    
    if db is not None:
        db.close() 


def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
