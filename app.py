#!/usr/bin/env python3.4

from FlaskApp import app, db, ConfigProduction, ConfigRemote
import Model
import argparse
import sys
import os.path

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--port', nargs=1, type=int, default=[80],
                           action='store')
    argparser.add_argument('-R', '--remote', action='store_true',
                           default=False)
    args = argparser.parse_args()
    if args.remote:
        app.config.from_object(ConfigRemote)
    else:
        app.config.from_object(ConfigProduction)
    db.create_all()
    app.run(host="0.0.0.0", port=args.port[0])
