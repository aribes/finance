import re
from . import utils

from . import utils_cfg
cfg = utils_cfg.cfg

def apply_regexes_to_data():

  regexes = utils.get_regexes()
  for regex in regexes:
    re_def   = regex[0]
    category = regex[1]
    p = re.compile(re_def)
    print('Running regex: {0} for category: {1}'.format(re_def, category))

    # Get All Raws
    all_rows = cfg.db_connection.execute('SELECT * FROM data')

    # Find rows to change
    rows_to_change = []
    for row in all_rows:
      if p.match(row[2]):
        rows_to_change.append(row)

    # Change categories to selected rows
    for row in rows_to_change:
        cfg.db_connection.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', (category, row[0], row[1], row[2]))

def apply_custom_regex():

  # Orthophoniste
  row_to_change = []
  p = re.compile('.*ATM.*')
  all_rows = cfg.db_connection.execute('SELECT * FROM data')
  for row in all_rows:
    if p.match(row[3]) and row[1] == -140.0:
      row_to_change.append(row)
  for row in row_to_change:
      cfg.db_connection.execute('UPDATE data SET category = ? WHERE date = ? AND amount = ? and description = ?', ('Orthophoniste', row[0], row[1], row[2]))

def run_regex(regex, tag, apply):
  p = re.compile(regex)
  all_rows = cfg.db_connection.execute('SELECT * FROM data')
  row_to_change = []
  for row in all_rows:
    if p.match(row[3]):
      row_to_change.append(row)
      if not apply: print(row)
  if not apply: return

  # Applying regex to rows
  for row in row_to_change:
      cfg.db_connection.execute('UPDATE data SET tags = ? WHERE date = ? AND amount = ? and description = ?', (tag, row[0], row[1], row[3]))

  # Adding regex to database
  cfg.db_connection.execute('INSERT INTO regexes VALUES (?,?)', (regex, tag))