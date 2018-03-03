import datetime
import re

def insert_csv_date_in_db(conn, cursor, pd):
  for _, row in pd.iterrows():
    str_format = '%Y-%m-%d'
    data = (datetime.datetime.strptime(row.date, '%d/%m/%Y').strftime(str_format), row.amount, row.description, row.acc_amount, row.bank_category)
    cursor.execute('INSERT INTO raw VALUES (?,?,?,?,?, "unknown", "unknown")', data)
  conn.commit()

def apply_regex_to_data(conn, cursor):
  regexes = cursor.execute('SELECT * FROM regex')
  regexes = regexes.fetchall()
  for regex in regexes:
    re_str   = regex[0]
    category = regex[1]
    print('Running regex:', re_str, ' for category:', category)

    p = re.compile(re_str)
    row_to_change = []
    all_raws = cursor.execute('SELECT * FROM raw')
    for row in all_raws:
      if p.match(row[2]):
        row_to_change.append(row)
    for row in row_to_change:
        cursor.execute('UPDATE raw SET category = ? WHERE date = ? AND amount = ? and description = ?', (category, row[0], row[1], row[2]))
  conn.commit()