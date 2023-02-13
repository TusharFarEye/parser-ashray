
from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint

baseSortCode = declarative_base()

class SortCodeMaster(baseSortCode):

    # def __init__(self):
    #     self.createdAt = None
    #     self.companyId = None
    #     self.sortCode = None
    #     self.pincode = None
    #     self.id = None
    __tablename__ = 'sort_code_master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pincode = Column(String)
    sort_code = Column(String)
    company_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    sort_code_syn = Column(String)
    UniqueConstraint(pincode, sort_code)

    def createObject(self, obj):
        # print(obj)
        # self.id = obj[0]
        self.pincode = obj[1]
        self.sort_code = obj[2]
        self.company_id = obj[3]
        self.created_at = obj[4]


def createSortCodeMasterFromArray(obj):
    arr = []
    for i in obj:
        scm = SortCodeMaster()
        scm.createObject(i)
        arr.append(scm)
    return arr
