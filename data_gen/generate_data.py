#! /usr/bin/env python2

import random
import uuid

import collections

from app.util import *
from werkzeug import generate_password_hash, check_password_hash
from random_words import RandomWords

rw = RandomWords()
random.seed()


def gen_students(db):
    with open('./data_gen/names.txt') as f:
        names = [
            (line.strip('\n').strip('\t').split(' ')) for line in f]

    query = ''
    for first, last in names:
        query += '''INSERT into students (personID, first, last) 
                        VALUES (0, '{}','{}');'''.format(first, last)

    return query


def gen_classes(db):
    query = ''

    query += '''INSERT INTO classes (className, startDate, endDate, startTime, endTIme, sun, mon, tue, wed, thu, fri, sat) VALUES 
('Leadership','')''' #MW
'Robotics' #MTWR
'Cooking' #R


def gen_lodging(db):
    with open('./data_gen/addresses.txt') as f:
        lines = [line.strip('').strip('\n') for line in f]
        addresses = [street + ' ' + city for street, city in zip(lines[::2], lines[1::2])]

    query = ''
    for addr in addresses:
        addr = "'" + addr.replace(',', '.') + "'"
        price = str(random.randint(500, 2000))
        url = "'" + 'https://www.lodging.com/' + str(uuid.uuid4().hex) + "'"
        query += " INSERT INTO lodging (lodgeID, price, address, url)" \
                 " VALUES (0, {}, {}, {});\n".format(price, addr, url)

    return query


def gen_groups(db):
    with open('./data_gen/group_names.txt') as f:
        group_names = ["'" + line.strip('\n').strip('\t') + "'" for line in f if line != "\n"]

    query = ''
    for gname in group_names:
        query += '''INSERT INTO groups (groupID, groupName) VALUES (0,{});\n'''.format(gname)
    return query


def gen_memberships(db):
    groupIDs = db.single_attr_query('SELECT groupID FROM groups;')
    personIDs = db.single_attr_query('SELECT personID FROM people;')

    query = ''
    for id in groupIDs:
        members = random.sample(personIDs, random.randint(3, 10))
        for m in members:
            query += '''INSERT INTO memberships (groupID, personID) VALUES ({},{});\n'''.format(id, m)

    # with open('out','w+') as f:
    #     f.write(query)
    return query


def gen_events(db):
    groupIDs = db.single_attr_query('SELECT groupID FROM groups;')
    random.shuffle(groupIDs)

    query = ''
    # Each group has at least one event
    for gid in groupIDs:
        name = ' '.join(rw.random_words(count=2))
        query += '''INSERT INTO events (eventID, groupID, eventName) VALUES (0,{},'{}');\n'''.format(gid, name)

    # Some groups have more than one, possible more than two
    for _ in range(0, int(.25 * len(groupIDs))):
        name = ' '.join(rw.random_words(count=2))
        gid = random.choice(groupIDs)
        query += '''INSERT INTO events (eventID, groupID, eventName) VALUES (0,{}, '{}');\n'''.format(gid, name)

    return query


def gen_voting_data(db):
    eventIDs = db.query('SELECT eventID, groupID FROM events;')
    lodgeIDs = db.single_attr_query('SELECT lodgeID FROM lodging;')

    with open('./data_gen/cities.txt') as f:
        cities = [l.split('\t')[2] for l in f]

    query = ''
    for event in eventIDs:
        people = db.single_attr_query('SELECT personID FROM memberships WHERE groupID = {};'.format(event[1]))

        for p in people:
            startd, stopd = getRandomPeriod(2017, 2017)
            startt, stopt = getRandomTimes()
            start = "'" + startd + startt + "'"
            stop = "'" + stopd + stopt + "'"

            query += '''INSERT INTO timerange(personID, eventID, start, stop) 
              VALUES( {}, {}, {}, {});\n'''.format(p, event[0], start, stop)

            bit = random.randint(0, 1)
            query += '''INSERT INTO commits(personID, eventID, groupID, decision)
              VALUES ({},{},{},{});\n'''.format(p, event[0], event[1], bit)

            location = random.choice(cities)
            locationID = add_location(db, location, event)

            lodge = random.choice(lodgeIDs)
            query += '''INSERT INTO votes(eventID, personID, groupID, lodgeVote, startVote, stopVote, locationVote)
              VALUES({},{},{},{},{},{},{});\n'''.format(event[0], p, event[1], lodge, start, stop, locationID)

    return query


def add_location(db, location, event):
    query = '''INSERT INTO locations(location, eventID) 
      VALUES( '{}', {});\n'''.format(location, event[0])
    print(query)
    db.query(query)
    return db.query('select LAST_INSERT_ID()')[0][0]


# Vote
def update_events(db):
    eventIDs = db.query('SELECT eventID, groupID FROM events;')

    query = ''
    for event in eventIDs:
        votes = db.query('SELECT personID,lodgeVote, startVote, stopVote, locationVote FROM votes '
                         'WHERE eventID = {};'.format(event[0]))

        locationIDs = collections.Counter([i[4] for i in votes])
        max_loc_id = max(locationIDs.keys(), key=lambda x:locationIDs[x])
        for loc in locationIDs.keys():
            query += '''UPDATE locations SET votes = {} 
            WHERE locationID = {};\n'''.format(locationIDs[loc],loc)

        commitCount = int(db.query('SELECT SUM(decision) from commits WHERE eventID = {}'.format(event[0]))[0][0])
        lodge = random.choice(votes)[1]
        admin = random.choice(votes)[0]

        # DATETIMES are bullshit
        start = "'" + random.choice(votes)[2].strftime('%Y-%m-%d %H:%M:%S') + "'"
        stop = "'" + random.choice(votes)[3].strftime('%Y-%m-%d %H:%M:%S') + "'"

        query += ''' UPDATE events SET lodgeID = {},start = {}, stop = {},confirmCount = {}, admin = {}, location = {}
            WHERE eventID = {};\n'''.format(lodge, start, stop, commitCount, event[0], admin, max_loc_id)
    return query


def get_functions():
    # return [gen_people, gen_lodging, gen_groups, gen_memberships,
    #         gen_events, gen_timerange, gen_commits]
    return [gen_people, gen_lodging, gen_groups, gen_memberships, gen_events, gen_voting_data, update_events]


if __name__ == '__main__':
    # gen_lodging()
    # gen_timerange()
    # gen_locations()
    pass


    # def gen_commits(db):
    #     eventIDs = db.query('SELECT eventID, groupID FROM events;')
    #
    #     query = ''
    #     for event in eventIDs:
    #         people = db.single_attr_query('SELECT personID FROM memberships WHERE groupID = {};'.format(event[1]))
    #         for p in people:
    #             bit = random.randint(0,1)
    #             query += '''INSERT INTO commits(personID, eventID, decision)
    #               VALUES ({},{},{});\n'''.format(p,event[0],bit)
    #
    #     return query
    #
    # # This can be combined with gen timerange
    # def gen_votes(db):
    #     eventIDs = db.query('SELECT eventID, groupID FROM events;')
    #
    #     query = ''
    #     for event in eventIDs:
    #         people = db.single_attr_query('SELECT personID FROM memberships WHERE groupID = {};'.format(event[1]))
    #             # random lodge
    #             # random location
    #
    #
    #             # their start time
    #             # their stop time