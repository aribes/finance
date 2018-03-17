import datetime
import re
import pandas

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

def apply_custom_recurrent(conn, cursor):
  all_raws = cursor.execute('SELECT * FROM raw')

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

def compute_statistics(conn, cursor, year, month, day):
  all_raws = cursor.execute('SELECT * FROM raw')
  df = pandas.DataFrame(all_raws.fetchall(), columns=['date', 'amount', 'description', 'acc_amount', 'bank_category', 'username', 'category'])
  df = df[df.category != 'Exclude']


  def keep_date(d, year=year, month=month, day=day):
    d_year  = d[:4]
    d_month = d[5:7]
    d_day   = d[8:]
    if year and d_year != year:
      return False
    if month and d_month != month:
      return False
    if day and d_day != day:
      return False
    return True

  df['keep'] = df.date.apply(keep_date)
  df = df[df.keep == True]
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

    print('----------------')
    print('Date:', group.date.iloc[0][:-3])
    print(data_per_category)
    print()
    print('Credit:',  credit)
    print('Debit:',   debit)
    print('Restant:', restant)
    print('Restant Projection:', restant_projection)
    print('----------------')