
from flask.ext.sqlalchemy import SQLAlchemy

class ConfigBase(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@127.0.0.1/housedowning"
    SECRET_KEY = "House Downing Secret Key - xylsi8dh7u19dws4ty63"
    USERNAME = 'webapp'
    PASSWORD = 'gotswe'

class ConfigProduction(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@127.0.0.1/housedowning"

class ConfigRemote(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@104.130.247.236/housedowning"

class ConfigTesting(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

db = SQLAlchemy()

def drop_all(db):
    """
    Manually drop all tables, if they exist.
    
    This is needed since the db.drop_all() statement is broken when using the
    postgresql backend engine. Unfortunately, this is very fragile and has to
    be manually updated any time the names of the tables used by our model
    changes.
    """
    print("Dropping all tables from {}".format(db))
    db.engine.execute("drop table if exists character cascade;")
    db.engine.execute("drop table if exists event cascade;")
    db.engine.execute("drop table if exists location cascade;")
    db.engine.execute("drop table if exists organization cascade;")
    db.engine.execute("drop table if exists membership cascade;")
    db.engine.execute("drop table if exists Participant cascade;")
    db.engine.execute("drop table if exists Party cascade;")
    db.engine.execute("drop table if exists Visitor cascade;")
