import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

sample_students = [
    {'name': 'Tanya Williams', 'key': 1},
    {'name': 'Katie Smith', 'key': 2},
    {'name': 'Bobby Hoover', 'key': 3},
    {'name': 'Kelly Fink', 'key': 4},
    {'name': 'Dian Stilts', 'key': 5},
    {'name': 'Chelsie Whitely', 'key': 6},
    {'name': 'Angelo Mendel', 'key': 7},
    {'name': 'Harvey Mancuso', 'key': 8},
    {'name': 'Cheri Swanigan', 'key': 9},
    {'name': 'Rodrick Stilson', 'key': 10},
    {'name': 'Andre Cornell', 'key': 11},
    {'name': 'Jordon Holstein', 'key': 12},
    {'name': 'Julietta Bustos', 'key': 13},
    {'name': 'Lanette Haskins', 'key': 14},
    {'name': 'Harry Kindred', 'key': 15},
    {'name': 'Kari Paine', 'key': 16},
    {'name': 'Jacquiline Keating', 'key': 17},
    {'name': 'Star Segawa', 'key': 18},
    {'name': 'Suanne Desimone', 'key': 19},
    {'name': 'Kayla Wentzel', 'key': 20},
    {'name': 'Emmy Spradley', 'key': 21},
    {'name': 'Marielle Kegley', 'key': 22},
    {'name': 'Maryalice Detrick', 'key': 23},
    {'name': 'Kendal Lund', 'key': 24},
    {'name': 'Luci Trumbull', 'key': 25},
    {'name': 'Alison Plascencia', 'key': 26},
    {'name': 'Kimberely Barba', 'key': 27},
    {'name': 'Maddie Ellinger', 'key': 28},
    {'name': 'Victor Pujol', 'key': 29},
    {'name': 'Celesta Jurgens', 'key': 30},
]

sample_roster = [
    {'name': 'Tanya Williams', 'key': 1, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 2, 'in': True, 'out': True},
    {'name': 'Bobby Hoover', 'key': 3, 'in': True, 'out': True},
    {'name': 'Kelly Fink', 'key': 4, 'in': True, 'out': False},
    {'name': 'Dian Stilts', 'key': 5, 'in': True, 'out': True},
    {'name': 'Chelsie Whitely', 'key': 6, 'in': True, 'out': True},
    {'name': 'Angelo Mendel', 'key': 7, 'in': True, 'out': True},
    {'name': 'Harvey Mancuso', 'key': 8, 'in': True, 'out': False},
    {'name': 'Cheri Swanigan', 'key': 9, 'in': True, 'out': True},
    {'name': 'Rodrick Stilson', 'key': 10, 'in': True, 'out': True},
    {'name': 'Andre Cornell', 'key': 11, 'in': True, 'out': True},
    {'name': 'Jordon Holstein', 'key': 12, 'in': True, 'out': False},
    {'name': 'Julietta Bustos', 'key': 13, 'in': True, 'out': True},
    {'name': 'Lanette Haskins', 'key': 14, 'in': True, 'out': True},
    {'name': 'Harry Kindred', 'key': 15, 'in': True, 'out': True},
    {'name': 'Kari Paine', 'key': 16, 'in': False, 'out': False},
    {'name': 'Jacquiline Keating', 'key': 17, 'in': True, 'out': True},
    {'name': 'Star Segawa', 'key': 18, 'in': False, 'out': False},
    {'name': 'Suanne Desimone', 'key': 19, 'in': False, 'out': False},
    {'name': 'Kayla Wentzel', 'key': 20, 'in': True, 'out': True},
    {'name': 'Emmy Spradley', 'key': 21, 'in': True, 'out': True},
    {'name': 'Marielle Kegley', 'key': 22, 'in': True, 'out': True},
    {'name': 'Maryalice Detrick', 'key': 23, 'in': True, 'out': True},
    {'name': 'Kendal Lund', 'key': 24, 'in': True, 'out': True},
    {'name': 'Luci Trumbull', 'key': 25, 'in': False, 'out': False},
    {'name': 'Alison Plascencia', 'key': 26, 'in': True, 'out': False},
    {'name': 'Kimberely Barba', 'key': 27, 'in': False, 'out': False},
    {'name': 'Maddie Ellinger', 'key': 28, 'in': True, 'out': True},
    {'name': 'Victor Pujol', 'key': 29, 'in': True, 'out': True},
    {'name': 'Celesta Jurgens', 'key': 30, 'in': True, 'out': False},
]

sample_classes = [
    {'name': 'Brain Health', 'key': 1},
    {'name': 'Leadership', 'key': 2},
    {'name': 'LEGO Robotics', 'key': 3},
    {'name': 'Shakespeare', 'key': 4},
    {'name': 'Tutoring', 'key': 5}
]

kelly = {
    'name': 'Kelly Fink',
    'dob': '11-11-10',
    'classes': ['Brain Health', 'LEGO Robotics', 'Shakespeare', 'Tutoring'],
    'signout': ['Permission to walk home.', 'Only parents may pick up.'],
    'emergency': [
        {'name': 'Harry Fink', 'number': '574-333-4444'},
        {'name': 'Sheila Fink', 'number': '574-555-5555'}
        ]
    }

@app.route('/', methods=['GET'])
def landing():
    if request.method == 'GET':
        return render_template('landing.html')


@app.route('/classes', methods=['GET'])
def classes():
    if request.method == 'GET':
        date = request.args.get('date', '')
        if date == '2018-04-18':
            return jsonify(sample_classes)
        else:
            return jsonify(sample_classes[::2])

    return jsonify([])


@app.route('/roster', methods=['GET'])
def roster():
    if request.method == 'GET':
        date = request.args.get('date', '')
        class_key = request.args.get('class', '')
        return jsonify(sorted(sample_roster, key=lambda s: s['name']))
    return jsonify([])


@app.route('/whoshere', methods=['GET'])
def whoshere():
    if request.method == 'GET':
        return jsonify(sorted(sample_students, key=lambda s: s['name']))

    return jsonify([])


@app.route('/student', methods=['GET'])
def student():
    if request.method == 'GET':
        student_key = request.args.get('student', '')
        return jsonify(kelly)
    return jsonify([])


@app.route('/rate', methods=['GET'])
def rate():
    if request.method == 'GET':
        return jsonify({'rate': random.randint(70, 100)})
    return jsonify({'rate': 0.0})
