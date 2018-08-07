import logging

from . import calc

log = logging.Logger()

def nicePrt(x):
  log.info('[{}] {} ({})'.format(x.date, x.description, x.amount))

def show_tags(data):
  tags = calc.get_tags(data)
  for tag in tags:
    log.info('Tag: {}'.format(tag))

def show_tags_content():
  show_tag_content(None)

def show_tag_content(tag):
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