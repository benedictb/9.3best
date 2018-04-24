#! /usr/bin/env python2
import yaml
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from app.db import DB
import json

from data_gen.generate_data import get_generators

config = yaml.load(open('rollcall.config'))
app = Flask(__name__)
db = DB(app, config)

app.config["DEBUG"] = True  # Only include this while you are testing your app


# Pages
@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('root.html')


@app.route('/reset', methods=['POST', 'GET'])  # Reset the database
def reset_db():
    res = db.reset()
    if request.method == 'GET':
        return render_template('reset.html')
    else:
        return res

@app.route('/generate', methods=['GET'])
def generate_db():
    db.reset()

    funcs = get_generators()
    for f in funcs:
        print f.__name__
        q = f(db)
        db.query(q)
    return render_template('generate.html')


@app.route('/studentProfile', methods=['POST', 'GET'])
def studentProfile():
    return render_template('studentProfile.html')

# gets

def getClasses():
    data = request.get_data()
    res = db.getClasses(data)
    return res


def getRoster():
    data = request.get_data()
    res = db.getRoster(data)
    return res


def getStudentsPresent():
    data = request.get_data()
    res = db.getStudentsPresent(data)
    return res


def getStudentDetail():
    data = request.get_data()
    res = db.getStudentDetail(data)
    return res


def getClassDetail():
    data = request.get_data()
    res = db.getClassDetail(data)
    return res


def getStatistics():
    data = request.get_data()
    res = db.getStatistics(data)
    return res


#  posts
@app.route('/', methods=['POST'])
def setStudentDetail():
    data = request.get_data()
    res = db.setStudentDetail(data)
    return res


# @app.route('/', methods=['POST'])
def setClassDetail():
    data = request.get_data()
    res = db.setClassDetail(data)
    return res


# @app.route('/', methods=['POST'])
def signin():
    data = request.get_data()
    res = db.signin(data)
    return res


# @app.route('/', methods=['POST'])
def signout():
    data = request.get_data()
    res = db.signout(data)
    return res


# @app.route('/', methods=['POST'])
def updateEnrollment():
    data = request.get_data()
    res = db.updateEnrollment(data)
    return res

@app.route('/attendanceRates', methods=['POST', 'GET'])
def attendanceRates():
    return render_template('attendanceRates.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
