from flask import Flask, request, jsonify
from db import db
import os

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
database_url = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url


# initialize the app with the sqlalchemy extension
db.init_app(app)
with app.app_context():
    db.create_all()

import hashing
def is_checksum_good(name, deaths, jumps, time, check):
    expected_check = hashing.generate_checksum(name, deaths, jumps, time)
    return expected_check == check


@app.route("/", methods = ["GET"])
def hello_world():
    return "Hello World"