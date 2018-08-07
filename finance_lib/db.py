# This module contains all the functions
# that the project needs to manipulate the data
# in the selected database

import sys
import logging
import pandas
import sqlite3
import re

class db_manager:

  self.log = logging.getLogger()

  def __init__(self, db_filename):
    self.db_connection = sqlite3.connect(db_filename)
    self.db_cursor = self.db_connection.cursor()
    self.init_db()

  def init_db(self):
    self.db_cursor.execute(
        'CREATE TABLE IF NOT EXISTS data (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, tags TEXT)')
    self.db_cursor.execute(
        'CREATE TABLE IF NOT EXISTS regex (regex TEXT, tag TEXT)')
    self.db_cursor.execute(
        'CREATE TABLE IF NOT EXISTS custom_tags (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, tags TEXT)')
    self.db_connection.commit()

  def get_data(self):
    log.info('Loading data from database')
    self.get_data_generic('data')
    log.info('Number of transactions: {}'.format(len(df.index)))
    return df

  def get_user_tags(self):
    log.info('Loading user\'s custom tags from database')
    self.get_data_generic('custom_tags')
    log.info('Number of custom tags: {}'.format(len(df.index)))
    return df

  def save_data(self, data):
    log.info('Saving data from database')
    self.save_data_generic('data')
    log.info('Done!')

  def save_custom_tags(self, data):
    log.info('Saving user\'s custom tags from database')
    self.save_data_generic('custom_tags')
    log.info('Done!')
  
  def get_data_generic(self, table_name):
    all_raws = self.db_cursor.execute('SELECT * FROM {}'.format(table_name))
    df = pandas.DataFrame(all_raws.fetchall(), columns=[
                          'date', 'amount', 'description', 'acc_amount', 'bank_category', 'username', 'tags'])
    return df

  def save_data_generic(self, table_name):
    # Erase all data from DB
    self.db_cursor.execute('DELETE FROM {}'.format(table_name))

    # Add all data from DB
    for _, row in data.iterrows():
      str_format = '%Y-%m-%d'
      data_to_insert = (table_name, datetime.strptime(row.date, '%d/%m/%Y').strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category, row.username, row.tags)
      self.db_cursor.execute('INSERT INTO ? VALUES (?,?,?,?,?,?,?)', data_to_insert)
    
    # Write in the database
    self.db_connection.commit()

  def get_regexes(self):
    log.info('Loading regexes from database')
    all_raws = self.db_cursor.execute('SELECT * FROM regex')
    df = pandas.DataFrame(all_raws.fetchall(), columns=['regex', 'tag'])
    df['re'] = df.regex.apply(lambda r : re.compile(r))
    log.info('Number of regexes: {}'.format(len(df.index)))
    return df

  def save_regexes(self, regexes):
    log.info('Saving regexes from database')
    # Erase all data from DB
    self.db_cursor.execute('DELETE FROM regex')

    # Add all data from DB
    for _, row in regexes.iterrows():
      data_to_insert = (row.regex, row.tag)
      self.db_cursor.execute('INSERT INTO regex VALUES (?,?)', data_to_insert)
    
    # Write in the database
    self.db_connection.commit()
    log.info('Done!')

  def disconnect(self):
    self.db_connection.close()
