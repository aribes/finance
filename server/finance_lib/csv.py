import pandas
from . import csv_loaders
from . import config


def import_bank_records_from_csv(filename):

  df = pandas.read_csv(filename)
  df = csv_loaders.load_records(df)

  if df is None:
    config.c.logger.warn("Could not detect CSV format file")
    config.c.logger.warn("Open CSV file and add parser to csv_loaders.py")

  return df
