# This module contains all the functions
# that the project needs to manipulate the data
# in the selected database

import sys
import logging
import pandas
import numpy
import sqlalchemy
import re

class db_manager:

  self.log = logging.getLogger()

  def __init__(self, db_url):
    self.db_url = db_url
    self.db = sqlalchemy.create_engine(self.db_url)
    self.init_db()

  def init_db(self):
    """
      Check if each table exists, if not create an empty pandas
      file with the desired columns and write into the database
    """

    if not self.db.dialect.has_table(self.db, 'data'):
      empty_df = pandas.DataFrame(
        columns=['date', 'amount', 'acc_amount', 'description', 'bank_category', 'username', 'tags'],
        dtype=['datetime64[ns]', numpy.float64, numpy.float64, 'object', 'object', 'object', 'object'])
      empty_df.to_sql('data', self.db)

    if not self.db.dialect.has_table(self.db, 'regexes'):
      empty_df = pandas.DataFrame(
        columns=['re_date', 're_amount', 're_acc_amount', 're_description', 're_bank_category', 're_username', 'tags'],
        dtype=['object', 'object', 'object', 'object', 'object', 'object', 'object'])
      empty_df.to_sql('regexes', self.db)

  def get_data(self):
    log.info('Loading data from database')
    return pandas.read_sql('data', self.db_url)

  def save_data(self, data):
    log.info('Saving data to database')
    data.to_sql('data', self.db, if_exists='replace')
    log.info('Done!')

  def get_regexes(self):
    log.info('Loading regexes from database')
    return pandas.read_sql('regexes', self.db_url)

  def save_regexes(self, regexes):
    log.info('Saving regexes to database')
    data.to_sql('regexes', self.db, if_exists='replace')
    log.info('Done!')
