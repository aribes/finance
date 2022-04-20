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
    print (pd.dtypes)
    pd = pd.astype({
       'description': str,
       'amount': float,
       'acc_amount': float})
    pd['date'] = pandas.to_datetime(pd['date'])
    pd['bank_category'] = ''
    return pd
  
  sys.exit('Unknow format {}'.format(version))

def add_pd_to_db(pd):
  for _, row in pd.iterrows():
    str_format = '%Y-%m-%d'
    data = (row.date.strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category)

    # Get SQLAlchemy Table
    # Insert only if does not exists from the data object 
    sel = select([literal("1"), literal("John")]).where(
           ~exists([example_table.c.id]).where(example_table.c.id == 1)
      )

ins = example_table.insert().from_select(["id", "name"], sel)
print(ins)
    cfg.db_connection.execute('INSERT INTO data VALUES (?,?,?,?,?, "unknown", "unknown")', data)