from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  

baseNonLableAdd = declarative_base()

class NonLabeledAddress(baseNonLableAdd):
    __tablename__ = 'non_labeled_address'

    address_id = Column(Integer, primary_key=True)
    address = Column(String)
    pincode = Column(String)
    processing_start_time = Column(TIMESTAMP)
    company_id = Column(Integer)
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP)
