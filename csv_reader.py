import pandas

def import_csv_file(filename):

  # CBA format 1
  # If need to add more banks then we will need to change
  # This format
  column_names = ['date', 'amount', 'description', 'acc_amount', 'bank_category']
  types        = {'amount': float, 'description': str, 'acc_amount': float, 'bank_category': str}
  return pandas.read_csv(filename, header=None, names=column_names, dtype=types)

def import_csv_credit_file(filename):

  # CBA Credit format 1
  # If need to add more banks then we will need to change
  # This format
  column_names = ['date', 'description', 'card', 'bank_category', 'amount']
  types        = {'amount': float, 'description': str, 'cart': str, 'bank_category': str}
  pd = pandas.read_csv(filename, header=None, names=column_names, dtype=types)
  pd['acc_amount'] = 0.0
  pd = pd.drop(['card'], axis='columns')
  return pd