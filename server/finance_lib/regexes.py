import re
from sqlalchemy.orm import Session
from . import db_tables
from . import config


def check_regex(regex, category):

  if category == '':
    config.c.logger.warn(f'Category is empty for regex {regex!r}')
    return False

  if not config.c.is_category_defined(category):
    config.c.logger.warn(f'Category cannot be found in the categories defined by the user {category!r}')
    return False

  try:
    re.compile(regex)
  except Exception as e:
    config.c.logger.warn(f'Regex does not compile {e!r}')
    return False

  return True


def run_regex(regex, category, apply_changes):
  p = re.compile(regex)
  with Session(config.c.engine) as session:
    for bankRecord in session.query(db_tables.BankRecord):
      if p.match(bankRecord.description):
        bankRecord.categories = category
        config.c.logger.info(f'Changed categaory of {bankRecord!r}')
    if apply_changes:
      session.commit()
