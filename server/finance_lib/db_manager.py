from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import db_tables
from . import config


class DatabaseManager:

  def __init__(self, db_url, echo=False):
    config.c.engine = create_engine(db_url, echo=echo, future=True)

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
