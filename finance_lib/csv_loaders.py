import pandas
from . import config


def load_bank_australia(df):
  if df.columns.tolist() == ['Effective Date',	'Entered Date',	'Transaction Description',	'Amount',	'Balance']:
    config.c.logger.info("Detected Bank Australia CSV file type")

    df = df.drop(['Effective Date'], axis='columns')
    df = df.rename(columns={
        'Entered Date': 'date',
        'Transaction Description': 'description',
        'Amount': 'amount',
        'Balance': 'account_amount'})
    df = df.astype({
        'description': str,
        'amount': float,
        'account_amount': float})
    df['date'] = pandas.to_datetime(df['date'], format='%d/%m/%Y')
    return df, True
  return df, False


def load_commonwealth_bank_of_australia(df):
  if df.columns.tolist() == ['date', 'amount', 'description', 'acc_amount', 'bank_category']:
    config.c.logger.info("Detected CBA CSV file type")

    df = df.drop(['bank_category'], axis='columns')
    df = df.rename(columns={'acc_amount': 'account_amount'})
    df = df.astype({
        'description': str,
        'amount': float,
        'account_amount': float})
    df['date'] = pandas.to_datetime(df['date'], format='%d/%m/%Y')
    return df, True
  return df, False


# TODO - Find a more pythonic way to write this code
def load_records(df):
  df, loaded = load_bank_australia(df)
  if loaded:
    return df
  df, loaded = load_commonwealth_bank_of_australia(df)
  if loaded:
    return df
