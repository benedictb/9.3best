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
    {'name': 'Bobby Hoover', 'key': 3, 'in': False, 'out': False}
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
        if date == '2018-04-17':
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
