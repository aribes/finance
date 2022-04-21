# This module contains all the functions
# that the project needs to manipulate the data
# in the selected database

import sys
import logging
import pandas
import numpy
import sqlalchemy
from sqlalchemy.orm import Session
import re

class db_manager:

  def __init__(self, db_url):
    self.log = logging.getLogger()
    self.db_url = 'sqlite:///' + db_url
    self.engine = sqlalchemy.create_engine(self.db_url)
    self.data_table = None
    self.regexes_table = None
    self.init_db()
    self.get_db_tables()

    # create session
    self.session = Session(self.engine)

  def init_db(self):
    """
      Check if each table exists, if not create an empty pandas
      file with the desired columns and write into the database
    """

    if not sqlalchemy.inspect(self.engine).has_table('data'):
      empty_df = pandas.DataFrame(columns=['date', 'amount', 'acc_amount', 'description', 'bank_category', 'username', 'tags'])
      empty_df = empty_df.astype({'amount': numpy.float64, 'acc_amount': numpy.float64})
      empty_df.to_sql('data', self.engine, index = False)

    if not sqlalchemy.inspect(self.engine).has_table('regexes'):
      empty_df = pandas.DataFrame(columns=['re_date', 're_amount', 're_acc_amount', 're_description', 're_bank_category', 're_username', 'tags'])
      empty_df.to_sql('regexes', self.engine, index = False)
  
  def get_db_tables(self):
    metadata = sqlalchemy.MetaData()
    metadata.reflect(bind=self.engine)
    self.data_table = metadata.tables['data']
    self.regexes_table = metadata.tables['regexes']

  def get_data(self):
    self.log.info('Loading data from database')
    return pandas.read_sql('data', self.db_url)

  def save_data(self, data):
    self.log.info('Saving data to database')
    data.to_sql('data', self.engine, if_exists='replace')
    self.log.info('Done!')

  def get_regexes(self):
    self.log.info('Loading regexes from database')
    return pandas.read_sql('regexes', self.db_url)

  def save_regexes(self, regexes):
    self.log.info('Saving regexes to database')
    regexes.to_sql('regexes', self.engine, if_exists='replace')
    self.log.info('Done!')
