from flask import Flask, request, jsonify
from db import db
import os
from models import *
from flask_cors import CORS, cross_origin

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
database_url = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url


#cors
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# initialize the app with the sqlalchemy extension
db.init_app(app)
with app.app_context():
    db.create_all()

import hashing
def is_timed_checksum_good(name, score, check):
    expected_check = hashing.generate_timed_checksum(name, score)
    return expected_check == check

def is_every_house_checksum_good(name, score, time, check):
    expected_check = hashing.generate_every_house_checksum(name, score, time)
    return expected_check == check



@app.route("/timed", methods = ["POST"])
@cross_origin()
def post_timed():
    name = request.form.get("name")
    score = request.form.get("score")
    checksum = request.form.get("checksum")
    if(is_timed_checksum_good(name, score, checksum)):
        print("checksum good")
        record_already_exists = len(db.session.query(TimedLeaderboard).filter_by(checksum=checksum).all())>0
        if not record_already_exists:
            leaderboard_record = TimedLeaderboard(name=name,score=score, checksum=checksum)
            db.session.add(leaderboard_record)
            db.session.commit()
        return "Done", 201
    return "Failed to authenticate", 401

@app.route("/timed", methods = ["GET"])
@cross_origin()
def get_timed():
    leaderboard_records = db.session.query(TimedLeaderboard).order_by(TimedLeaderboard.score.desc())
    output = []
    for record in leaderboard_records:
        output.append(
            {
                "name":record.name,
                "score":record.score
            }
        )
    return jsonify({"entries":output}), 200

@app.route("/every_house", methods= ["POST"])
def post_every_house():
    name = request.form.get("name")
    score = request.form.get("score")
    time = request.form.get("time")
    checksum = request.form.get("checksum")
    if(is_every_house_checksum_good(name, score, time, checksum)):
        print("checksum good")
        record_already_exists = len(db.session.query(EveryHouseLeaderboard).filter_by(checksum=checksum).all())>0
        if not record_already_exists:
            leaderboard_record = EveryHouseLeaderboard(name=name,score=score,time=time,checksum=checksum)
            db.session.add(leaderboard_record)
            db.session.commit()
        return "Done", 201
    return "Failed to authenticate", 401

@app.route("/every_house", methods=["GET"])
def get_every_house():
    leaderboard_records = db.session.query(EveryHouseLeaderboard).order_by(EveryHouseLeaderboard.score.desc())
    output = []
    for record in leaderboard_records:
        output.append(
            {
                "name":record.name,
                "score":record.score,
                "time":record.time
            }
        )
    return jsonify({"entries":output}), 200