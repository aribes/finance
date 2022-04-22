from sqlalchemy import Column, Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import PrimaryKeyConstraint

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BankRecord(Base):
   __tablename__ = "bank_record"
   __table_args__ = (
    PrimaryKeyConstraint('date', 'amount', 'account_amount', 'description', name='bank_record_pk'),
   )
   
   date = Column(String)
   amount = Column(Float)
   account_amount = Column(Float)
   description = Column(String)
   categories = Column(String, default='')


   def __repr__(self):
     return f"BankRecord(date={self.date!r}, amount={self.amount!r}, account_amount={self.account_amount!r}, description={self.description!r})"


# TODO - Have a pre-check to ensure that the provided regex can be compiled
class Categoriser(Base):
   __tablename__ = 'categoriser'

   id = Column(Integer, primary_key=True)
   regex = Column(String)
   category = Column(String)

   def __repr__(self):
    return f"Categoriser(id={self.id!r}, regex={self.regex!r}, category={self.category!r}"