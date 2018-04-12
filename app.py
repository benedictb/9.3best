#! /usr/bin/env python2
import yaml
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from app.db import DB


config = yaml.load(open('rollcall.config'))
app = Flask(__name__)
db = DB(app, config)

app.config["DEBUG"] = True  # Only include this while you are testing your app


# Pages
@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('root.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")