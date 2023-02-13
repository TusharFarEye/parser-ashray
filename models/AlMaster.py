from json import JSONEncoder
from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseAlMaster = declarative_base()

class AlMaster(baseAlMaster):

    __tablename__ = 'al_master'

    id = Column(Integer, primary_key=True)
    al1 = Column(String)
    al2 = Column(String)
    al3 = Column(String)
    pincode = Column(String)
    country_code = Column(String)
    company_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    UniqueConstraint(al1, al2, al3, pincode, company_id, country_code)
    

    def default(self, o):
        return o.__dict__

    # def __init__(self):
    #     self.createdAt = None
    #     self.countryCode = None
    #     self.companyId = None
    #     self.pincode = None
    #     self.al3 = None
    #     self.al2 = None
    #     self.al1 = None
    #     self.id = None
    def createObject(self, obj):
        self.id = obj[0]
        self.al1 = obj[3]
        self.al2 = obj[2]
        self.al3 = obj[1]
        self.pincode = obj[4]
        self.companyId = obj[5]
        self.countryCode = obj[6]
        self.createdAt = obj[7]
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)
    def toObject(self):
        return {"id": self.id,"al1":self.al1,"al2":self.al2,"al3":self.al3,"pincode":self.pincode}


def createAlmasterFromArray(obj):
    arr = []
    for i in obj:
        al = AlMaster()
        al.createObject(i)
        arr.append(al)
    return arr

def getObjectFromArray(obj):
    arr = []
    for i in obj:
        arr.append(i.toObject())
    return arr
