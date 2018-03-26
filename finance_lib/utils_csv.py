from datetime import datetime
import pandas
import sys

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

  sys.exit('Unknow format {}'.format(version))

def add_csv_to_db(pd):
  for _, row in pd.iterrows():
    str_format = '%Y-%m-%d'
    data = (datetime.strptime(row.date, '%d/%m/%Y').strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category)
    cfg.db_cursor.execute('INSERT INTO raw VALUES (?,?,?,?,?, "unknown", "unknown")', data)
  cfg.db_connection.commit()