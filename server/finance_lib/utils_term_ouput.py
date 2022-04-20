from . import utils

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
  groups = df.groupby(['category'])
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
    print('Restant Projection:', month_stats['restant_proj'])
    print('----------------')