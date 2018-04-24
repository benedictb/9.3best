#! /usr/bin/env python2

import random
from datetime import date, timedelta

import uuid

import collections

from random_words import RandomWords

from app.util import weekList

rw = RandomWords()
random.seed()


def gen_students(db):
    with open('./data_gen/names.txt') as f:
        names = [
            (line.strip('\n').strip('\t').split(' ')) for line in f]

    query = ''
    for first, last in names:
        query += '''INSERT into students (studentID, firstName, lastName) 
                        VALUES (0, '{}','{}');\n'''.format(first, last)

    return query


def gen_classes(db):
    query = ''

    # Hardcode a few classes
    query += '''INSERT INTO classes (className, startDate, endDate, startTime, endTime, mon, wed) VALUES 
    ('Leadership','2018-1-15', '2018-6-30', '16:00','17:00', 1,1);\n'''  # MW

    query += '''INSERT INTO classes (className, startDate, endDate, startTime, endTime, mon, tue, wed, thu) VALUES 
    ('Robotics','2018-2-1', '2018-5-24', '17:00','18:00', 1,1,1,1);\n'''  # MW

    query += '''INSERT INTO classes (className, startDate, endDate, startTime, endTime, thu) VALUES 
    ('Cooking','2018-1-30', '2018-8-16', '15:00','16:00', 1);\n'''  # MW

    return query


def gen_enrollment(db):
    students = db.query('SELECT studentID, firstName, lastName FROM students;')
    classIDs = db.query('SELECT classID FROM classes;')

    query = ''
    for student in students:
        c = random.choice(classIDs)
        print(c)
        query += '''INSERT INTO enrollment (classID, studentID, firstName, lastName) VALUES ({},{},'{}','{}');\n'''.format(
            c['classID'], student['studentID'], student['lastName'], student['firstName'])

    return query


def gen_attendance(db):
    d1 = date(2018, 4, 15)  # start date
    d2 = date(2018, 5, 15)  # end date
    daynames = weekList()

    classes = db.query('SELECT * FROM classes ORDER BY classID')
    rosters = dict()

    for c in classes:
        rosters[c['classID']] = db.query('SELECT * FROM enrollment where classID = {}'.format(c['classID']))

    starts = [16, 17, 15]

    query = ''

    delta = d2 - d1  # timedelta
    for i in range(delta.days + 1):
        d = d1 + timedelta(days=i)
        dayname = daynames[d.weekday()]

        for i, c in enumerate(classes):
            if c[dayname]:
                for student in rosters[c['classID']]:
                    if random.randint(1, 4) > 1:
                        start = ' ' + str(starts[i]) + ':' + str(random.randint(0, 59)) + ':' + str(
                            random.randint(0, 59))
                        stop = ' ' + str(starts[i] + 1) + ':' + str(
                            random.randint(0, 59)) + ':' + str(random.randint(0, 59))
                        startDT = d.strftime('%Y-%-m-%d') + start
                        stopDT = d.strftime('%Y-%-m-%d') + stop

                        print startDT

                        query += '''INSERT INTO attendance (classID, inTime, outTime, studentID) VALUES ({}, '{}', '{}', {});\n'''.format(
                            c['classID'], startDT, stopDT, student['studentID'])
    return query

def get_generators():
    return [gen_students, gen_classes, gen_enrollment, gen_attendance]