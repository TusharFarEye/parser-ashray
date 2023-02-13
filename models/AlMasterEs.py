from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseAlMasterEs = declarative_base()

class AlMasterEs(baseAlMasterEs):
    __tablename__ = 'al1_master'

    al1 = Column(String)
    al1Syn = Column(String)
    al2 = Column(String)
    al2Syn = Column(String)
    al3 = Column(String)
    al3Syn = Column(String)
    pincode = Column(String)
    company_id = Column(Integer)
    UniqueConstraint(al1,al2,al3,pincode,company_id)

'''al1 text,
   al1Syn text,
   al2 text,
   al2Syn text,
   al3 text,
   al3Syn text,
   pincode text,
   company_id int,
   UNIQUE(al1,al2,al3,pincode,company_id)
'''