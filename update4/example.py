from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

sample_students = [
    {'name': 'Tanya Williams', 'key': 1},
    {'name': 'Katie Smith', 'key': 2},
    {'name': 'Bobby Hoover', 'key': 3}
]

sample_roster = [
    {'name': 'Tanya Williams', 'key': 1, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 2, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 3, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 4, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 5, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 6, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 7, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 8, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 9, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 10, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 11, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 12, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 13, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 14, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 15, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 16, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 17, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 18, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 19, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 20, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 21, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 22, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 23, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 24, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 25, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 26, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 27, 'in': False, 'out': False},
    {'name': 'Tanya Williams', 'key': 28, 'in': True, 'out': True},
    {'name': 'Katie Smith', 'key': 29, 'in': True, 'out': False},
    {'name': 'Bobby Hoover', 'key': 30, 'in': False, 'out': False},
]

sample_classes = [
    {'name': 'Brain Health', 'key': 1},
    {'name': 'Leadership', 'key': 2},
    {'name': 'LEGO Robotics', 'key': 3},
    {'name': 'Shakespeare', 'key': 4},
    {'name': 'Tutoring', 'key': 5}
]


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
        return jsonify(sample_roster)
    return jsonify([])


@app.route('/whoshere', methods=['GET'])
def whoshere():
    if request.method == 'GET':
        return jsonify(sample_students)

    return jsonify([])


@app.route('/student', methods=['GET'])
def student():
    if request.method == 'GET':
        student_key = request.args.get('student', '')
        return jsonify('student data')
    return jsonify([])
