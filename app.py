#!/usr/bin/env python3.4

from FlaskApp import app, db
import Model
import argparse
import sys
import os.path

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--port', nargs=1, type=int, default=[80],
                           action='store')
    args = argparser.parse_args()
    #db.create_all()
    #app.run(port=8080)
    app.run(host="0.0.0.0", port=args.port[0])
