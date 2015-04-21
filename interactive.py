
from FlaskApp import *
from app import *
from Model import *

app.config.from_object(ConfigRemote)
db.init_app(app)
ctx = app.test_request_context()

ctx.push()

