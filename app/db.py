import datetime
from flask import session, jsonify
from flaskext.mysql import MySQL
import json
from pymysql.cursors import DictCursor

from app.util import deserialize, weekList, formatDays


# TODO fix getStudentsPresent, getroster, app.util.getdays, might need INT casts but prob not
# also - put a restriction on signing into classes that don't occur on the day of the week that they are scheduled


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
        days = formatDays(d['days'])

        res = self.query('''INSERT INTO classes (className, startDate, endDate, startTime, endTime, sun, mon, tue, wed, thu, fri, sat) VALUES 
                          VALUES ({},'{}','{}', '{}', '{}',{}) '''.format(
            d['className'], d['startDate'], d['endDate'], d['startTime'], d['endTime'], ','.join(
                [str(x) for x in days])))

        new_id = self.query('select LAST_INSERT_ID()')[0][0]
        return jsonify({'valid': 'true', 'id': new_id})

    def signin(self, data):
        d = deserialize(data)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        res = self.query(
            '''INSERT into attendance (classID, studentID, inTime, inDate ) VALUES ({},{},'{}')'''.format(
                d['classID'], d['studentID'], now, today
            )
        )
        return jsonify({'valid': 'true'})

    def signout(self, data):
        d = deserialize(data)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = now.date()

        res = self.query('''UPDATE attendance SET outTime = '{}' WHERE classID = {} AND studentID = {} AND 
                              DATE(inTime) = '{}'; '''.format(now, d['classID'], d['studentID'], today))

        return jsonify({'valid': 'true'})

    # GETs

    def getClassDetail(self, data):
        d = deserialize(data)
        res = self.query(
            '''SELECT * FROM classes WHERE classID = {}'''.format(
                d['classID']
            )
        )

        return jsonify(res)

    def getStudentDetail(self, data):
        d = deserialize(data)
        res = self.query(
            '''SELECT * FROM students WHERE studentID = {}'''.format(
                d['studentID']
            )
        )

        return jsonify(res)  # SELECT * from students where studentID = {}

    # Examine
    def getStudentsPresent(self, data):
        d = deserialize(data)

        # Only want people that have signed in this day in case there's some discrepancies
        fdate = datetime.datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S')
        sdate = fdate.strftime('%Y-%m-%d')

        res = self.query(
            '''SELECT studentID, firstName, lastName FROM attendence a, students s where a.studentID = s.studentID 
            and a.inDate = '{}' AND (a.outTime IS NOT NULL OR a.outTime > '{}' '''.format(
                sdate, d['date']
            )
        )

        return jsonify(res)

    def getClasses(self, data):
        d = deserialize(data)

        # Please enter as "YYYY-MM-DD"
        qdate = d['date']
        sdate = datetime.date.strftime(d['date'], '%Y-%M-%D')
        dayname = weekList()[sdate.weekday()]

        res = self.query(
            '''SELECT * FROM classes WHERE {} = 1 AND startDate <= '{}' and endDate >= '{}'; '''.format(
                dayname, qdate, qdate
            )
        )

        return jsonify(res)

    def getRoster(self, data):
        d = deserialize(data)

        res = self.query(
            '''SELECT * FROM enrollment e LEFT OUTER JOIN attendance a ON (e.studentID = a.studentID) and e.classID = {}
            AND inDate = '{}';'''.format(
                d['classID'], d['date']
            )
        )

        return jsonify(res)

    #



    # This one's slightly more complicated
    def getStatistics(self, data):
        d = deserialize(data)

        # possible addition --- don't count days that no one signed in for at all - no class that day
        # Get no of days that class was in attendance
        dayNames = weekList()

        startDate = datetime.datetime.strptime(d['startDate'], '%Y-%m-%d')
        endDate = datetime.datetime.strptime(d['endDate'], '%Y-%m-%d')

        day_counts = dict(zip(dayNames, [0] * 7))

        td = datetime.timedelta(days=1)
        while startDate <= endDate:
            day_counts[dayNames[startDate.weekday()]] += 1
            startDate += td

        # Get num of enrolled students, need debugging for this
        roster_length = self.query(
            '''SELECT COUNT(*) FROM enrollment WHERE classID = {}'''.format(
                d['classID']
            )
        )

        # Get total num of days this class was in session between the start and end date inclusive
        total_days = 0
        for day in d['days']:
            total_days += day_counts[day]

        # Get total number of students that could have possible been there
        possible = total_days * roster_length

        # Get total number of students that were actually there
        actual = self.query(
            '''SELECT COUNT(*) FROM attendance WHERE dayOfWeek IN ({}) AND inDate >= '{}' AND inDate <= '{}' '''.format(
                formatDays(d['days']), d['startDate'], d['endDate']
            )
        )

        ratio = float(actual) / float(possible)

        return jsonify({'value': ratio})



    # UPDATE

    def updateEnrollment(self, data):
        pass

    def retroactiveSignin(self):
        pass

    def retroactiveSignout(self):
        pass
