from . import utils
from . import config
from . import db_tables

from sqlalchemy.orm import Session

def nicePrt(x):
  print('[',x.date,'] ', x.description, ' (', x.amount, ')')

def show_categories():
  categories = utils.get_categories()
  for cat in categories:
    print(cat)

def show_categories_content():
  show_category_content(None)

def show_category_content(category):
  df = utils.get_data()
  groups = df.groupby(['categories'])
  for name, group in groups:
    if category and name != category:
      continue
    print('----------------')
    print('Category:', name)
    print()
    group.apply(nicePrt, axis='columns')
    print('----------------')
    print()

def show_statistics():
  statistics = utils.get_statistics()

  for month_stats in statistics:
    print('----------------')
    print('Date:', month_stats['date'])
    print(month_stats['category_amount'])
    print()
    print('Credit:',  month_stats['credit'])
    print('Debit:',   month_stats['debit'])
    print('Restant:', month_stats['restant'])
    print()
    print('----------------')


def show_categorisers():
  with Session(config.c.engine) as session:
    for categoriser in session.query(db_tables.Categoriser).order_by(db_tables.Categoriser.category):
      print('| Category: {: <15} || Regex: {: <40} || Id: {: <5} |'.format(categoriser.category, categoriser.regex, categoriser.id))
