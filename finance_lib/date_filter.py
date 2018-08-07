from datetime import datetime
import sys

class date_filter:

  self.wanted_year   = None
  self.wanted_month  = None
  self.wanted_day    = None

  def __init__(self, date_str):
    self.load_date(date_str)

  def filter(self, data):
    data['keep'] = data.date.apply(self._keep_date)
    data = data[data.keep == True]
    return data

  def _load_date(self, date_str):
    if not date_str:
      return

    try:
      extracted_date = datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
      try:
        extracted_date = datetime.strptime(date_str, '%Y%m')
      except ValueError:
        try:
          extracted_date = datetime.strptime(date_str, '%Y')
        except ValueError:
          sys.exit("Unknown date, please use: 2018, 201801 or 20180101")
        else:
          self.wanted_year  = extracted_date.strftime('%Y')
      else:
        self.wanted_year  = extracted_date.strftime('%Y')
        self.wanted_month = extracted_date.strftime('%m')
    else:
      self.wanted_year  = extracted_date.strftime('%Y')
      self.wanted_month = extracted_date.strftime('%m')
      self.wanted_day   = extracted_date.strftime('%d')

  def _keep_date(self, row):
    year  = row[:4]
    month = row[5:7]
    day   = row[8:]
    if self.wanted_year and year != self.wanted_year:
      return False
    if self.wanted_month and month != self.wanted_month:
      return False
    if self.wanted_day and day != self.wanted_day:
      return False
    return True