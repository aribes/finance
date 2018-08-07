import re
from . import utils

from . import utils_cfg
cfg = utils_cfg.cfg

def apply_regexes_to_data(data, regexes):

  regexes = utils.get_regexes()
  for regex in regexes:
    re_def   = regex[0]
    category = regex[1]
    p = re.compile(re_def)
    print('Running regex: {0} for category: {1}'.format(re_def, category))

    # Get All Raws
    all_rows = cfg.db_cursor.execute('SELECT * FROM raw')

    # Find rows to change
    rows_to_change = []
    for row in all_rows:
      if p.match(row[2]):
        rows_to_change.append(row)

    # Change categories to selected rows
    for row in rows_to_change:
        cfg.db_cursor.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', (category, row[0], row[1], row[2]))

  cfg.db_connection.commit()

def run_regex(regex, category, apply):
  p = re.compile('.*ATM.*')
  all_rows = cfg.db_cursor.execute('SELECT * FROM raw')
  row_to_change = []
  for row in all_rows:
    if p.match(row[2]):
      row_to_change.append(row)
      if not apply: print(row)
  if not apply: return

  # Applying regex to rows
  for row in row_to_change:
      cfg.db_cursor.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', (args.regex_category, row[0], row[1], row[2]))
  cfg.db_connection.commit()

  # Adding regex to database
  cfg.db_cursor.execute('INSERT INTO regex VALUES (?,?)', (regex, category))
  cfg.db_connection.commit()