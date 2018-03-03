#!/usr/bin/env python3

# TODO - Clean raw of month / year before inserting again CSV data
# TODO - Replace category table
# TODO - Cash debit table

import re
import argparse
from datetime import datetime

import pandas
import sqlite3

import csv_reader
import utils

db_filename = "test.db"

parser = argparse.ArgumentParser()
parser.add_argument("--add_csv_file", help="Add CSV file to the database")
parser.add_argument("--add_csv_credit_file", help="Add CSV from credit mastercard file to the database")
parser.add_argument("--test_regex", help="Test New Regex", action="store_true")
parser.add_argument("--apply_regex", help="Apply New Regex", action="store_true")
parser.add_argument("--regex_category", help="New Regex Category")
parser.add_argument("--regex_definition", help="New Regex Definition")
args = parser.parse_args()


conn = sqlite3.connect(db_filename)
c = conn.cursor()

# Checking if Table exists, if not create it
c.execute('CREATE TABLE IF NOT EXISTS raw (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, category TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS regex (regex TEXT, category TEXT)')
conn.commit()

if args.add_csv_file:
  print('Adding CSV file to the database:', args.add_csv_file)
  pd = csv_reader.import_csv_file(args.add_csv_file)
  utils.insert_csv_date_in_db(conn, c, pd)
  utils.apply_regex_to_data(conn, c)

if args.add_csv_credit_file:
  print('Adding CSV credit file to the database:', args.add_csv_credit_file)
  pd = csv_reader.import_csv_credit_file(args.add_csv_credit_file)
  utils.insert_csv_date_in_db(conn, c, pd)
  utils.apply_regex_to_data(conn, c)

if args.test_regex and args.regex_category and args.regex_definition:
  print("Testing regex cat:", args.regex_category, " def:", args.regex_definition)

  p = re.compile(args.regex_definition)

  result = c.execute('SELECT * FROM raw')
  for row in result:
    if p.match(row[2]):
      print(row)

if args.apply_regex and args.regex_category and args.regex_definition:
  print("Applying regex cat:", args.regex_category, " def:", args.regex_definition)
  p = re.compile(args.regex_definition)
  result = c.execute('SELECT * FROM raw')
  row_to_change = []
  for row in result:
    if p.match(row[2]):
      row_to_change.append(row)
  for row in row_to_change:
      c.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', (args.regex_category, row[0], row[1], row[2]))
  conn.commit()

  # Adding regex to database
  c.execute('INSERT INTO regex VALUES (?,?)', (args.regex_definition, args.regex_category))
  conn.commit()

conn.close()