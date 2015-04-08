#!/usr/bin/env python3.4

from FlaskApp import db, ConfigRemote, ConfigProduction, drop_all
import argparse
import sys
import os.path

# We don't actively use anything from these, but it is important to import them
# to load the changes they make to the database and app objects.
import Model
import Routing
from Routing import app

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-m', '--make-tables', action='store_true',
                           default=False, dest='maketables')
    argparser.add_argument('-p', '--port', nargs=1, type=int, default=[80],
                           action='store')
    argparser.add_argument('-R', '--remote', action='store_true',
                           default=False)
    argparser.add_argument('-d', '--database', nargs=1, type=str,
                           action='store', default=['HouseDowning'])
    
    args = argparser.parse_args()
    if args.remote:
        app.config.from_object(ConfigRemote)
    else:
        app.config.from_object(ConfigProduction)
    
    db.init_app(app)

    if args.maketables:
        drop_all(db, app)
        db.create_all(app=app)
        #import_data(db)
    app.run(host="0.0.0.0", port=args.port[0])
