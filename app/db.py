import datetime
from flask import session, jsonify
from flaskext.mysql import MySQL
import json
from pymysql.cursors import DictCursor

from app.util import deserialize, getDays


class DB(object):
    """Database connection and gateway for the API calls"""

    def __init__(self, app, config):
        mysql = MySQL(cursorclass=DictCursor)

        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = config['user']
        app.config['MYSQL_DATABASE_PASSWORD'] = config['mysql_password']
        app.config['MYSQL_DATABASE_DB'] = config['database']
        app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
        mysql.init_app(app)
        self.mysql = mysql
        self.conn = mysql.connect()

    # Database management
    def reset(self):
        query = open('./resources/schema.sql').read()
        curr = self.conn.cursor()
        curr.execute(query)
        res = curr.fetchall()
        self.conn.commit()

        if len(res) is 0:
            return json.dumps({'message': 'Database reset successfully !'})
        else:
            return json.dumps({'error': str(res)})

    def query(self, q):
        print q
        cur = self.conn.cursor()
        cur.execute(q)
        res = cur.fetchall()
        self.conn.commit()
        return res

    # POSTs

    def setStudentDetail(self, data):
        d = deserialize(data)
        res = self.query('''INSERT into students (firstName, lastName, pictureURL, birthday, iceName, icePhone, signOutInfo) 
                          VALUES ({}, {}, {}, {}, {}, {}, {});'''.format(d['firstName', d['lastName'], d['pictureURL'],
                                                                           d['birthday'], d['iceName'], d['icePhone'],
                                                                           d['signOutInfo']]))
        new_id = self.query('select LAST_INSERT_ID()')[0][0]
        return jsonify({'valid': 'true', 'id': new_id})

    def setClassDetail(self, data):
        d = deserialize(data)
        days = getDays(d['days'])

        res = self.query('''INSERT INTO classes (className, startDate, endDate, startTime, endTIme, sun, mon, tue, wed, thu, fri, sat) VALUES 
                          VALUES ({},'{}','{}', '{}', '{}',{}) '''.format(
            d['className'], d['startDate'], d['endDate'], d['startTime'], d['endTime'], ','.join(
                [str(x) for x in days])))

        new_id = self.query('select LAST_INSERT_ID()')[0][0]
        return jsonify({'valid': 'true', 'id': new_id})

    def signin(self, data):
        d = deserialize(data)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = self.query('''INSERT into attendence (classID, studentID) VALUES ({},{},'{}')'''.format(d['classID'],
                                                                                                      d['studentID'],
                                                                                                      now))
        return jsonify({'valid': 'true'})

    def signout(self, data):
        d = deserialize(data)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = now.date()

        res = self.query('''UPDATE attendance SET outTime = '{}' WHERE classID = {} AND studentID = {} AND 
                              DATE(inTime) = '{}'; '''.format(now, d['classID'], d['studentID'], today))

        return jsonify({'valid': 'true'})

    # UPDATE

    def updateEnrollment(self, data):
        pass

    def retroactiveSignin(self):
        pass

    def retroactiveSignout(self):
        pass

    # GETs

    def getStatistics(self, data):
        d = deserialize(data)
        # length = len("SELECT COUNT(*) from class_membership where classID = {CLASS_ID}

    def getClassDetail(self, data):
        pass
        # SELECT * from classes where classID = {}

    def getStudentDetail(self, data):
        pass
        # SELECT * from students where studentID = {}

    def getStudentsPresent(self, data):
        pass

    # SELECT studentID, firstName, lastName FROM attendence a, students s where a.studentID = a.studentID
    # and a.inTime < currTime and a.outTime is NOT NULL

    def getRoster(self, data):
        d = deserialize(data)
        res = self.query(
            '''SELECT a.firstName, a.lastName FROM attendance a  '''.format(location, eventID))

    # select roster
    # SELECT firstName, lastName, studentID, inTime, outTime FROM class_membership LEFT JOIN attendance ON studentID
    # WHERE classID = {CLASS_ID} and CAST(inTime AS DATE) = {QUERY_DATE}

    def getClasses(self, data):
        d = deserialize(data)

        res = self.query(
            '''SELECT classID, className, days '''.format(location, eventID))
        # get the current day of the week

        # SELECT classID, className, startTime, endTime FROM classes WHERE {} = 1
