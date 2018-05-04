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


@app.route('/')



@app.route('/studentProfile', methods=['POST', 'GET'])
def studentProfile():
    return render_template('studentProfile.html')


@app.route('/classes', methods=['POST'])
def getClasses():
    """
    Retrieves the class information for a given date
    params: date (format YYYY-MM-DD)
    """
    data = request.form
    res = db.getClasses(data)
    return res


def getRoster():
    """
    Retrieves the enrollment for a particular class
    params: classID, date (format YYYY-MM-DD)
    """
    data = request.form
    res = db.getRoster(data)
    return res

@app.route('/studentsPresent', methods=['POST'])
def getStudentsPresent():
    """
    Retrieves all students present at a given time
    params: datetime (format YYYY-MM-DD HH:MM:SS)
    """
    data = request.form
    res = db.getStudentsPresent(data)
    return res

@app.route('/studentDetail', methods=['POST'])
def getStudentDetail():
    """
    Retrieves information for a particular student
    params: studentID
    """
    data = request.form
    res = db.getStudentDetail(data)
    return res

@app.route('/classDetail', methods=['POST'])
def getClassDetail():
    """
    Retrieves information for a particular class
    params: classID
    """
    
    data = request.form
    res = db.getClassDetail(data)
    return res


def getStatistics():
    """
    Retrieves the attendance statistic for a given timeframe,
    class and list of days
    params: startDate (format YYYY-MM-DD), endDate,
            days ( format list of days requested in first-three-letter format
            eg: ['mon', 'wed', 'thu'] )
    """
    data = request.form
    res = db.getStatistics(data)
    return res


#  posts
@app.route('/', methods=['POST'])
def setStudentDetail():
    """
    Creates a new student
    params: (all strings) firstName, lastName, pictureURL, birthday, iceName,
            icePhone, signOutInfo
    """
    data = request.form
    res = db.setStudentDetail(data)
    return res


# @app.route('/', methods=['POST'])
def setClassDetail():
    """
    Creates a new class
    params: className,
            startDate (format YYYY-MM-DD), endDate,
            startTime (format HH:MM:SS), endTime,
            sun (1 for True, 0 for False), mon, tue, wed, thu, fri, sat
    """
    data = request.form
    res = db.setClassDetail(data)
    return res


# @app.route('/', methods=['POST'])
def signin():
    """
    Signs a student in
    params: studentID, classID
    """
    data = request.form
    res = db.signin(data)
    return res


# @app.route('/', methods=['POST'])
def signout():
    """
    Signs a student in
    params: studentID, classID
    """
    data = request.form
    res = db.signout(data)
    return res


# UPDATEs
# (not yet implemented)

# @app.route('/', methods=['POST'])
def updateEnrollment():
    data = request.form
    res = db.updateEnrollment(data)
    return res

def retroactiveSignin(self):
    data = request.form
    res = db.updateEnrollment(data)
    return res

def retroactiveSignout(self):
    data = request.form
    res = db.updateEnrollment(data)
    return res




@app.route('/attendanceRates', methods=['POST', 'GET'])
def attendanceRates():
    return render_template('attendanceRates.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
