from flask import session, jsonify
from flaskext.mysql import MySQL


class DB(object):
    """docstring for ClassName"""

    def __init__(self, app, config):
        mysql = MySQL()

        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = config['user']
        app.config['MYSQL_DATABASE_PASSWORD'] = config['mysql_password']
        # app.config['MYSQL_DATABASE_DB'] = config['database']
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