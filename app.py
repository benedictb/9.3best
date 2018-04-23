#! /usr/bin/env python2
import yaml
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from app.db import DB
import json


config = yaml.load(open('rollcall.config'))
app = Flask(__name__)
db = DB(app, config)

app.config["DEBUG"] = True  # Only include this while you are testing your app


# Pages
@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('root.html')

@app.route('/reset', methods=['POST', 'GET']) #Reset the database 
def reset_db():
    res = db.reset()
    if request.method == 'GET':
        return render_template('reset.html')
    else:
        return res


@app.route('/studentProfile', methods=['POST', 'GET'])
def studentProfile():
    return render_template('studentProfile.html')

@app.route('/attendanceRates', methods=['POST', 'GET'])
def attendanceRates():
    return render_template('attendanceRates.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")