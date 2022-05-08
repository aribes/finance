import sys
import re
import pandas

from sqlalchemy.orm import Session
from . import db_tables
from . import config

from . import utils_cfg
cfg = utils_cfg.cfg

def get_data():
  with Session(config.c.engine_1_4) as session:
    df = pandas.read_sql(session.query(db_tables.BankRecord).statement, session.bind)
    return df

def get_categories():
  df = get_data()
  return df.category.unique()

def get_statistics():
  statistics = []
  df = get_data()
  df = df[df.categories != 'Exclude']

  # Detect year/months and print for each one
  df['date_filter'] = df.date.apply(lambda x : x[:-3])
  df_groups_date = df.groupby(['date_filter'])
  for name, group in df_groups_date:

    data_per_category = group.groupby(['categories']).agg({'amount': sum})
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