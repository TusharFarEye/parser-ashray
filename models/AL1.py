from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseAl1 = declarative_base()

class AL1(baseAl1):
    __tablename__ = 'al1_master'

    al1 = Column(String, primary_key=True)
    syn = Column(String)
    company_id = Column(Integer, primary_key=True)
    UniqueConstraint(al1, company_id)

    def make(self, arr):
        self.al1=arr[0]
        self.syn=arr[1]
        self.company_id=arr[2]