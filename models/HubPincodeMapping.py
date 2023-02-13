from sqlalchemy import Column, String, Integer, TIMESTAMP, ARRAY
from sqlalchemy.ext.declarative import declarative_base  

baseHubPin = declarative_base()

class HubPinMap(baseHubPin):
    __tablename__ = 'hub_pincode_mapping'

    company_id = Column(Integer, primary_key=True)
    hub_id = Column(String, primary_key=True)
    pincode = Column(ARRAY(String))
    created_at = Column(TIMESTAMP)

