#!/usr/bin/env python3

import configparser
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