#!/usr/bin/env python3

import configparser
import json
import finance_lib.db as fl_db

config = configparser.ConfigParser()
config.read('finance_srv.ini')

# Connecting to DB
db_manager = fl_db.db_manager(config['db']['url'])

data = db_manager.get_data()
regexes = db_manager.get_regexes()

# Starting Flask Server
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

state = 0
@app.route('/')
def hello_world():
    global state
    rtn_str = 'Welcome to finance server - test number {}'.format(state)
    state += 1
    return jsonify(rtn_str)

@app.route('/load', methods = ['POST'])
def load_raw_data():
    print(request.headers['Content-Type'])
    print(request)
    if request.headers['Content-Type'] == 'application/json':
        print ("Hello")
        print (request.data)
        print (request.json)
        print("JSON Message: {}".format(json.dumps(request.json)))
        return jsonify('ok')
    return jsonify('Error')