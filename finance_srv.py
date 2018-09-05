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
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to finance server'