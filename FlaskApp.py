
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Response
import json

class ConfigBase(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:gotswe@127.0.0.1/housedowning"
    SECRET_KEY = "House Downing Secret Key - xylsi8d:gotswh7u19dws4ty63"
    USERNAME = 'webapp'
    PASSWORD = 'gotswe'

class ConfigProduction(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:gotswe@127.0.0.1/housedowning"

class ConfigRemote(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:gotswe@67.192.246.60/housedowning"

class ConfigTesting(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

db = SQLAlchemy()

def import_data(db, app, rawpath):
    pass

def json_response(obj):
    return Response(json.dumps(obj), mimetype='application/json')

def drop_all(db, app):
    """
    Manually drop all tables, if they exist.
    
    This is needed since the db.drop_all() statement is broken when using the
    postgresql backend engine. Unfortunately, this is very fragile and has to
    be manually updated any time the names of the tables used by our model
    changes.
    """
    ctx = app.test_request_context()
    ctx.push()
    
    db.engine.execute("drop table if exists character cascade;")
    db.engine.execute("drop table if exists event cascade;")
    db.engine.execute("drop table if exists location cascade;")
    db.engine.execute("drop table if exists organization cascade;")
    db.engine.execute("drop table if exists episode cascade;")
    db.engine.execute("drop table if exists membership cascade;")
    db.engine.execute("drop table if exists participant cascade;")
    db.engine.execute("drop table if exists party cascade;")
    db.engine.execute("drop table if exists visitor cascade;")
    
    ctx.pop()
