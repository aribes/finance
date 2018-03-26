import sys
import re
import pandas

from . import utils_cfg
cfg = utils_cfg.cfg

def get_regexes():
  regexes = cfg.db_cursor.execute('SELECT * FROM regex')
  return regexes.fetchall()

def get_data():
  all_raws = cfg.db_cursor.execute('SELECT * FROM raw')
  df = pandas.DataFrame(all_raws.fetchall(), columns=['date', 'amount', 'description', 'acc_amount', 'bank_category', 'username', 'category'])
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
    debit_proj = -9400 + group[group.category != 'Loyer'][group.amount <= 0.0].amount.sum()
    restant_projection = credit + debit_proj
    statistics.append({
       'date': name
      ,'category_amount': data_per_category
      ,'credit': credit
      ,'debit': debit
      ,'restant':restant
      ,'debit_proj': debit_proj
      ,'restant_proj': restant_projection
      ,'df': group
    })

  return statistics