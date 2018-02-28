#!/usr/bin/env python3

# TODO - Clean database of month / year before inserting again CSV data

import pandas

db_filename = "test.db"


import argparse
import csv_reader

parser = argparse.ArgumentParser()
parser.add_argument("--add_csv_file", help="Add CSV file to the database")
args = parser.parse_args()


import sqlite3
conn = sqlite3.connect(db_filename)
c = conn.cursor()

# Checking if Table exists, if not create it
c.execute('CREATE TABLE IF NOT EXISTS raw (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT)')
conn.commit()

if args.add_csv_file:
  print('Adding CSV file to the database:', args.add_csv_file)
  pd = csv_reader.import_csv_file(args.add_csv_file)

  # Change columns types
  for idx, row in pd.iterrows():
    str_format = '%Y-%m-%d'
    data = (pandas.Timestamp(row.date).strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category)
    c.execute('INSERT INTO raw VALUES (?,?,?,?,?)', data)
  conn.commit()

conn.close()