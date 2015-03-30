
from flask import Flask
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
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@104.130.247.236/HouseDowningTesting"

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(ConfigBase)


