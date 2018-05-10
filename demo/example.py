import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

sample_students = [
    {'lastName': 'Williams', 'firstName': 'Tanya', 'key': 1},
    {'lastName': 'Smith', 'firstName': 'Katie', 'key': 2},
    {'lastName': 'Hoover', 'firstName': 'Bobby', 'key': 3},
    {'lastName': 'Fink', 'firstName': 'Kelly', 'key': 4},
    {'lastName': 'Stilts', 'firstName': 'Dian', 'key': 5},
    {'lastName': 'Whitely', 'firstName': 'Chelsie', 'key': 6},
    {'lastName': 'Mendel', 'firstName': 'Angelo', 'key': 7},
    {'lastName': 'Mancuso', 'firstName': 'Harvey', 'key': 8},
    {'lastName': 'Swanigan', 'firstName': 'Cheri', 'key': 9},
    {'lastName': 'Stilson', 'firstName': 'Rodrick', 'key': 10},
    {'lastName': 'Cornell', 'firstName': 'Andre', 'key': 11},
    {'lastName': 'Holstein', 'firstName': 'Jordon', 'key': 12},
    {'lastName': 'Bustos', 'firstName': 'Julietta', 'key': 13},
    {'lastName': 'Haskins', 'firstName': 'Lanette', 'key': 14},
    {'lastName': 'Kindred', 'firstName': 'Harry', 'key': 15},
    {'lastName': 'Paine', 'firstName': 'Kari', 'key': 16},
    {'lastName': 'Keating', 'firstName': 'Jacquiline', 'key': 17},
    {'lastName': 'Segawa', 'firstName': 'Star', 'key': 18},
    {'lastName': 'Desimone', 'firstName': 'Suanne', 'key': 19},
    {'lastName': 'Wentzel', 'firstName': 'Kayla', 'key': 20},
    {'lastName': 'Spradley', 'firstName': 'Emmy', 'key': 21},
    {'lastName': 'Kegley', 'firstName': 'Marielle', 'key': 22},
    {'lastName': 'Detrick', 'firstName': 'Maryalice', 'key': 23},
    {'lastName': 'Lund', 'firstName': 'Kendal', 'key': 24},
    {'lastName': 'Trumbull', 'firstName': 'Luci', 'key': 25},
    {'lastName': 'Plascencia', 'firstName': 'Alison', 'key': 26},
    {'lastName': 'Barba', 'firstName': 'Kimberely', 'key': 27},
    {'lastName': 'Ellinger', 'firstName': 'Maddie', 'key': 28},
    {'lastName': 'Pujol', 'firstName': 'Victor', 'key': 29},
    {'lastName': 'Jurgens', 'firstName': 'Celesta', 'key': 30},
]

sample_roster = [
    {'lastName': 'Williams', 'firstName': 'Tanya', 'key': 1, 'in': True, 'out': True},
    {'lastName': 'Smith', 'firstName': 'Katie', 'key': 2, 'in': True, 'out': True},
    {'lastName': 'Hoover', 'firstName': 'Bobby', 'key': 3, 'in': True, 'out': True},
    {'lastName': 'Fink', 'firstName': 'Kelly', 'key': 4, 'in': True, 'out': False},
    {'lastName': 'Stilts', 'firstName': 'Dian', 'key': 5, 'in': True, 'out': True},
    {'lastName': 'Whitely', 'firstName': 'Chelsie', 'key': 6, 'in': True, 'out': True},
    {'lastName': 'Mendel', 'firstName': 'Angelo', 'key': 7, 'in': True, 'out': True},
    {'lastName': 'Mancuso', 'firstName': 'Harvey', 'key': 8, 'in': True, 'out': False},
    {'lastName': 'Swanigan', 'firstName': 'Cheri', 'key': 9, 'in': True, 'out': True},
    {'lastName': 'Stilson', 'firstName': 'Rodrick', 'key': 10, 'in': True, 'out': True},
    {'lastName': 'Cornell', 'firstName': 'Andre', 'key': 11, 'in': True, 'out': True},
    {'lastName': 'Holstein', 'firstName': 'Jordon', 'key': 12, 'in': True, 'out': False},
    {'lastName': 'Bustos', 'firstName': 'Julietta', 'key': 13, 'in': True, 'out': True},
    {'lastName': 'Haskins', 'firstName': 'Lanette', 'key': 14, 'in': True, 'out': True},
    {'lastName': 'Kindred', 'firstName': 'Harry', 'key': 15, 'in': True, 'out': True},
    {'lastName': 'Paine', 'firstName': 'Kari', 'key': 16, 'in': False, 'out': False},
    {'lastName': 'Keating', 'firstName': 'Jacquiline', 'key': 17, 'in': True, 'out': True},
    {'lastName': 'Segawa', 'firstName': 'Star', 'key': 18, 'in': False, 'out': False},
    {'lastName': 'Desimone', 'firstName': 'Suanne', 'key': 19, 'in': False, 'out': False},
    {'lastName': 'Wentzel', 'firstName': 'Kayla', 'key': 20, 'in': True, 'out': True},
    {'lastName': 'Spradley', 'firstName': 'Emmy', 'key': 21, 'in': True, 'out': True},
    {'lastName': 'Kegley', 'firstName': 'Marielle', 'key': 22, 'in': True, 'out': True},
    {'lastName': 'Detrick', 'firstName': 'Maryalice', 'key': 23, 'in': True, 'out': True},
    {'lastName': 'Lund', 'firstName': 'Kendal', 'key': 24, 'in': True, 'out': True},
    {'lastName': 'Trumbull', 'firstName': 'Luci', 'key': 25, 'in': False, 'out': False},
    {'lastName': 'Plascencia', 'firstName': 'Alison', 'key': 26, 'in': True, 'out': False},
    {'lastName': 'Barba', 'firstName': 'Kimberely', 'key': 27, 'in': False, 'out': False},
    {'lastName': 'Ellinger', 'firstName': 'Maddie', 'key': 28, 'in': True, 'out': True},
    {'lastName': 'Pujol', 'firstName': 'Victor', 'key': 29, 'in': True, 'out': True},
    {'lastName': 'Jurgens', 'firstName': 'Celesta', 'key': 30, 'in': True, 'out': False},
]

sample_tutors = [
    {
        'lastName': 'Phillips',
        'firstName': 'Doug',
        'key': 1, 'in': True,
        'students': [
            {'firstName': 'Kelly', 'lastName': 'Fink', 'key': 4, 'in': True, 'out': False},
            {'firstName': 'Tanya', 'lastName': 'Williams', 'key': 1, 'in': True, 'out': False}
            ],
    },
    {
        'lastName': 'Middleton',
        'firstName': 'Charles',
        'key': 2,
        'in': False,
        'students': [
            {'lastName': 'Barba', 'firstName': 'Kimberely', 'key': 27, 'in': False, 'out': False},
            {'lastName': 'Ellinger', 'firstName': 'Maddie', 'key': 28, 'in': True, 'out': False}
            ],
    },
]

sample_classes = [
    {'name': 'Brain Health', 'key': 1},
    {'name': 'Leadership', 'key': 2},
    {'name': 'LEGO Robotics', 'key': 3},
    {'name': 'Shakespeare', 'key': 4},
    {'name': 'Tutoring', 'key': 5}
]

kelly = {
    'firstName': 'Kelly',
    'lastName': 'Fink',
    'dob': '08-21-10',
    'classes': ['Brain Health', 'LEGO Robotics', 'Shakespeare', 'Tutoring'],
    'signout': ['Permission to walk home.', 'Only parents may pick up.'],
    'emergency': [
        {'name': 'Harry Fink', 'number': '574-333-4444'},
        {'name': 'Sheila Fink', 'number': '574-555-5555'}
        ]
    }

tanya = {
    'firstName': 'Tanya',
    'lastName': 'Williams',
    'dob': '03-12-10',
    'classes': ['Leadership', 'Shakespeare', 'Tutoring'],
    'signout': ['Can be signed out by John Williams.'],
    'emergency': [
        {'name': 'Joe Williams', 'number': '574-435-4324'},
        {'name': 'Jen Williams', 'number': '574-435-8243'}
        ]
    }


doug = {
    'firstName': 'Doug',
    'lastName': 'Phillips',
    'students': [
        {'firstName': 'Kelly', 'lastName': 'Fink', 'key': 4},
        {'firstName': 'Tanya', 'lastName': 'Williams', 'key': 1}
        ],
    'days': ['Monday', 'Wednesday', 'Thursday'],
    'email': 'dphillip@nd.edu',
    'phone': '474-222-3472'
    }


@app.route('/', methods=['GET'])
def landing():
    if request.method == 'GET':
        return render_template('landing.html')


@app.route('/classes', methods=['GET'])
def classes():
    if request.method == 'GET':
        date = request.args.get('date', '')
        if date == '2018-05-11':
            return jsonify(sample_classes)
        else:
            return jsonify(sample_classes[::2])

    return jsonify([])


@app.route('/roster', methods=['GET'])
def roster():
    if request.method == 'GET':
        date = request.args.get('date', '')
        class_key = int(request.args.get('class', ''))
        if class_key == 5:
            return jsonify(sorted(sample_tutors, key=lambda s: s['lastName']))
        return jsonify(sorted(sample_roster, key=lambda s: s['lastName']))
    return jsonify([])


@app.route('/whoshere', methods=['GET'])
def whoshere():
    if request.method == 'GET':
        return jsonify(sorted(sample_students, key=lambda s: s['lastName']))

    return jsonify([])

@app.route('/directory', methods=['GET'])
def directory():
    if request.method == 'GET':
        return jsonify(sorted(sample_students, key=lambda s: s['lastName']))

    return jsonify([])

@app.route('/student', methods=['GET'])
def student():
    if request.method == 'GET':
        student_key = int(request.args.get('student', ''))
        if student_key == 1:
            return jsonify(tanya)
        return jsonify(kelly)
    return jsonify([])

@app.route('/tutor', methods=['GET'])
def tutor():
    if request.method == 'GET':
        tutor_key = request.args.get('tutor', '')
        return jsonify(doug)
    return jsonify([])

@app.route('/rate', methods=['GET'])
def rate():
    if request.method == 'GET':
        return jsonify({'rate': random.randint(70, 100)})
    return jsonify({'rate': 0.0})
