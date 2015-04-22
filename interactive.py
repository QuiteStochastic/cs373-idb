
from FlaskApp import *
from app import *
from Model import *

import atexit

ctx = None

def start(config=ConfigProduction):
    global ctx
    
    app.config.from_object(config)
    db.init_app(app)
    ctx = app.test_request_context()
    ctx.push()
    atexit.register(end)

def end():
    global ctx
    
    if ctx is not None:
        ctx.pop()
        ctx = None
