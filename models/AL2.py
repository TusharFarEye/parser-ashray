from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseAl2 = declarative_base()

class AL2(baseAl2):
    __tablename__ = 'al2_master'

    al2 = Column(String, primary_key=True)
    syn = Column(String)
    company_id = Column(Integer, primary_key=True)
    UniqueConstraint(al2, company_id)

    def make(self, arr):
        self.al2=arr[0]
        self.syn=arr[1]
        self.company_id=arr[2]