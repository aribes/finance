from datetime import datetime
import pandas
import sys
import logging
from sqlalchemy import *

from . import utils_cfg
cfg = utils_cfg.cfg

def import_csv_file(filename, version=''):

  # Main format of CBA from savings account
  if version == 'cba_1':
    # CBA format 1
    # If need to add more banks then we will need to change
    # This format
    column_names = ['date', 'amount', 'description', 'acc_amount', 'bank_category']
    types        = {'amount': float, 'description': str, 'acc_amount': float, 'bank_category': str}
    return pandas.read_csv(filename, header=None, names=column_names, dtype=types)

  # Format of CBA from credit card account 
  if version == 'cba_2':
    column_names = ['date', 'description', 'card', 'bank_category', 'amount']
    types        = {'amount': float, 'description': str, 'cart': str, 'bank_category': str}
    pd = pandas.read_csv(filename, header=None, names=column_names, dtype=types)
    pd = pd.drop(['card'], axis='columns')
    pd['acc_amount'] = 0.0
    return pd

  # Try to auto detect the type
  pd = pandas.read_csv(filename)
  if pd.columns.tolist() == ['Effective Date',	'Entered Date',	'Transaction Description',	'Amount',	'Balance']:
    logging.info("Detected Bank Australia CSV file type")
    pd = pd.drop(['Effective Date'], axis='columns')
    pd = pd.rename(columns={
      'Entered Date': 'date',
      'Transaction Description': 'description',
      'Amount': 'amount',
      'Balance': 'acc_amount'})
    pd = pd.astype({
       'description': str,
       'amount': float,
       'acc_amount': float})
    pd['date'] = pandas.to_datetime(pd['date'], format='%d/%m/%Y')
    pd['bank_category'] = ''
    return pd
  
  sys.exit('Unknow format {}'.format(version))

def add_pd_to_db(pd):
  for _, row in pd.iterrows():
    
    # TODO - Move that somewhere else
    str_format = '%Y-%m-%d'
    data = (row.date.strftime(str_format), row.amount, row.acc_amount, row.description, row.bank_category)
    
    filtered =  cfg.session.query(cfg.data_table).filter_by(
      date = data[0],
      amount = data[1],
      acc_amount = data[2],
      description = data[3]).first()
    
   
    if filtered is None:
      print ("Adding new data in the database", data)
      cfg.db_connection.execute('INSERT INTO data VALUES (?,?,?,?,?, "", "")', data)
    else:
      print ("Data already found in the database", data)
    