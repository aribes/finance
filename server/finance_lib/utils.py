import sys
import re
import pandas

from . import utils_cfg
cfg = utils_cfg.cfg

# Checking if Table exists, if not create it
def init_db():
  cfg.db_connection.execute('CREATE TABLE IF NOT EXISTS raw (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, category TEXT)')
  cfg.db_connection.execute('CREATE TABLE IF NOT EXISTS custom (date TEXT, amount REAL, description TEXT, acc_amount REAL, bank_category TEXT, username TEXT, category TEXT)')
  cfg.db_connection.execute('CREATE TABLE IF NOT EXISTS regex (regex TEXT, category TEXT)')
  cfg.db_connection.commit()

def get_regexes():
  regexes = cfg.db_connection.execute('SELECT * FROM regexes')
  return regexes.fetchall()

def get_data():
  all_raws = cfg.db_connection.execute('SELECT * FROM data')
  df = pandas.DataFrame(all_raws.fetchall(), columns=['date', 'amount', 'acc_amount', 'description', 'bank_category', 'username', 'category'])
  return cfg.filter(df)

def get_categories():
  df = get_data()
  return df.category.unique()

def get_statistics():
  statistics = []
  df = get_data()
  df = df[df.category != 'Exclude']

  # Detect year/months and print for each one
  df['date_filter'] = df.date.apply(lambda x : x[:-3])
  df_groups_date = df.groupby(['date_filter'])
  for name, group in df_groups_date:

    data_per_category = group.groupby(['category']).agg({'amount': sum})
    credit  = group[group.amount > 0.0].amount.sum()
    debit   = group[group.amount <= 0.0].amount.sum()
    restant = credit + debit
    statistics.append({
       'date': name
      ,'category_amount': data_per_category
      ,'credit': credit
      ,'debit': debit
      ,'restant':restant
      ,'df': group
    })

  return statistics