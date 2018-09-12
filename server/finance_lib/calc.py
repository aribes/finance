import sys
import re
import pandas

# Checking if Table exists, if not create it
def get_categories():
  df = get_data()
  return df.category.unique()

def get_statistics():
  statistics = []
  df = get_data()
  df = df[df.category != 'Exclude']

  # Detect year/months and print for each one
  df['date_filter'] = df.date.apply(lambda x: x[:-3])
  df_groups_date = df.groupby(['date_filter'])
  for name, group in df_groups_date:

    data_per_category = group.groupby(['category']).agg({'amount': sum})
    credit = group[(group.amount > 0.0) & (
        group.amount < 20000.0)].amount.sum()
    debit = group[(group.amount <= 0.0) & (
        group.amount > -20000.0)].amount.sum()
    restant = credit + debit

    to_transfer = -1700
    if name < "2018-04":
      to_transfer = -9400
    debit_proj = to_transfer + \
        group[group.category != 'Loyer'][group.amount <= 0.0].amount.sum()
    restant_projection = credit + debit_proj
    statistics.append({
        'date': name, 'category_amount': data_per_category, 'credit': credit, 'debit': debit, 'restant': restant, 'debit_proj': debit_proj, 'restant_proj': restant_projection, 'df': group
    })

  return statistics
