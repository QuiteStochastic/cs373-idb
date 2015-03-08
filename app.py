#!/usr/bin/env python3.4

from flask import Flask, Response, render_template
import sys
import os.path

DATABASE = "./house-downing.db"
DEBUG = True
SECRET_KEY = "House Downing Secret Key - xylsi8dh7u19dws4ty63"
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def main_page():
    """
    Serve the main page from ./templates/main.html
    """
    return render_template("main.html")

@app.route('/about')
def about_page():
    """
    Serve the about page from ./templates/about.html
    """
    return render_template("about.html")

@app.route('/contact')
def contact_page():
    """
    Serve the contact page from ./temlates/contact.html
    """
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(port=8080)
