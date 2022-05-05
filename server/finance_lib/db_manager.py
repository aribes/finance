import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import db_tables
from . import config


class DatabaseManager:

  def __init__(self, db_url, echo=False):
    config.c.engine = create_engine(db_url, echo=echo, future=True)
    config.c.engine_1_4 = create_engine(db_url, echo=echo, future=False)
 
    # This will not recreate the tables it they already exists
    db_tables.Base.metadata.create_all(config.c.engine)

  def add_bank_records(self, df):

    with Session(config.c.engine) as session:

      records_to_add = []
      # Not the greatest way to use pandas... but we need to check that the record is not already in the database
      for _, row in df.iterrows():

        record = db_tables.BankRecord(
          date=row.date.strftime(config.c.date_format),
          amount=row.amount,
          account_amount=row.account_amount,
          description=row.description)

        filtered = session.query(db_tables.BankRecord).filter_by(
          date=record.date,
          amount=record.amount,
          account_amount=record.account_amount,
          description=record.description).first()

        if filtered is None:
          config.c.logger.info(f"Adding new data in the database: {record!r}")
          records_to_add.append(record)
        else:
          config.c.logger.info(f"Bank record already found in the database: {record!r}")

      session.add_all(records_to_add)
      session.commit()
      
  def add_categoriser(self, regex, category):

    with Session(config.c.engine) as session:
      
      categoriser = db_tables.Categoriser(
        regex=regex,
        category=category)
      
      filtered = session.query(db_tables.Categoriser).filter_by(
        regex=regex,
        category=category).first()

      if filtered is None:
        config.c.logger.info(f"Adding new categoriser in the database: {categoriser!r}")
        session.add(categoriser)
        
      session.commit()

  def export_categorisers(self, csv_filename):
    config.c.logger.info('Export categorisers to a CSV file: {}'.format(csv_filename))
    with Session(config.c.engine_1_4) as session:
      df = pd.read_sql(session.query(db_tables.Categoriser).statement, session.bind)
      df.to_csv(csv_filename, index=False, sep=";")

  def import_categorisers(self, csv_filename):
    config.c.logger.info('Import categorisers from a CSV file: {}'.format(csv_filename))
    df = pd.read_csv(csv_filename, sep=";")
    df.to_sql(db_tables.Categoriser.__tablename__, con=config.c.engine_1_4, if_exists='replace', index=False)
