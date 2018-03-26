import re
from . import utils

from . import utils_cfg
cfg = utils_cfg.cfg

def apply_regexes_to_data():

  regexes = utils.get_regexes(cfg.db_cursor)
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

def apply_custom_regex(conn, cursor):
  # Orthophoniste
  row_to_change = []
  p = re.compile('.*ATM.*')
  all_raws = cursor.execute('SELECT * FROM raw')
  for row in all_raws:
    if p.match(row[2]) and row[1] == -140.0:
      row_to_change.append(row)
  for row in row_to_change:
      cursor.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', ('Orthophoniste', row[0], row[1], row[2]))
  conn.commit()