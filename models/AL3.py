from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseAl3 = declarative_base()

class AL3(baseAl3):
    __tablename__ = 'al3_master'

    al3 = Column(String, primary_key=True)
    syn = Column(String)
    company_id = Column(Integer, primary_key=True)
    UniqueConstraint(al3, company_id)

    def make(self, arr):
        self.al3=arr[0]
        self.syn=arr[1]
        self.company_id=arr[2]