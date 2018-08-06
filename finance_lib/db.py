# This module contains all the functions
# that the project needs to manipulate the data
# in the selected database

import pandas
from . import utils_cfg
cfg = utils_cfg.cfg


def init_db():
  cfg.db_cursor.execute(
      'CREATE TABLE IF NOT EXISTS data (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, tags TEXT)')
  cfg.db_cursor.execute(
      'CREATE TABLE IF NOT EXISTS regex (regex TEXT, tag TEXT)')
  cfg.db_connection.commit()

def get_regexes():
  regexes = cfg.db_cursor.execute('SELECT * FROM regex')
  return regexes.fetchall()

def get_data():
  all_raws = cfg.db_cursor.execute('SELECT * FROM data')
  df = pandas.DataFrame(all_raws.fetchall(), columns=[
                        'date', 'amount', 'description', 'acc_amount', 'bank_category', 'username', 'tags'])
  return cfg.filter(df)

def save_data(pd):
  # Erase all data from DB
  cfg.db_cursor.execute('DELETE FROM data')

  # Add all data from DB
  for _, row in pd.iterrows():
    str_format = '%Y-%m-%d'
    data = (datetime.strptime(row.date, '%d/%m/%Y').strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category, row.username, row.tags)
    cfg.db_cursor.execute('INSERT INTO raw VALUES (?,?,?,?,?,?,?)', data)
  
  cfg.db_connection.commit()