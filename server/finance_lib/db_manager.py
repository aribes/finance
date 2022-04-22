import logging
import pandas
import sqlalchemy
from sqlalchemy.orm import Session

from . import db_tables


class DatabaseManager:

  def __init__(self, db_url, echo=False):
    self.log = logging.getLogger()
    self.engine = sqlalchemy.create_engine(db_url, echo=echo, future=True)
   
    # This will not recreate the tables it they already exists 
    db_tables.Base.metadata.create_all(self.engine)