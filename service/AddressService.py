from service.Connections import *
from .parser.thaiParser import ThaiParser
from service.AddressParse import *
from models.HubPincodeMapping import HubPinMap
from models.NonLabeledAddress import NonLabeledAddress
from models.AL1 import AL1
from models.AL2 import AL2
from models.AL3 import AL3
from models.SortCodeMaster import SortCodeMaster
from datetime import datetime, timedelta
from sqlalchemy import select, update
import aiohttp

def fetchNext(TempProxy): 
    temp = TempProxy.fetchmany(30)
    print(temp)

    return temp

def getAddressByCompanyIdAndHubId(company_id, hub_id, user_id):
    
    company_id = int(company_id)

    pinTemp = session.query(HubPinMap.pincode).filter_by(company_id=company_id).filter_by(hub_id=hub_id).all()

    # if (len(pinTemp)==0): return []
    
    count = 0
    result = {}

    address=[]
    idList=[]
    data = {}
    data['parserName'] = "thaiParser"
    data['address'] ={}
    returnResult = []
     
    time_difference = datetime.now() - timedelta(hours=1)
    
    temp1 = ["12", "234"]
    # it return the first 30 rows and the after calling again it fetch next 30 rows, and so on;
    query = (
        select(NonLabeledAddress.address, NonLabeledAddress.address_id, NonLabeledAddress.pincode)
        .where(NonLabeledAddress.company_id==company_id)
        .where(NonLabeledAddress.pincode.in_(temp1))
        .where(NonLabeledAddress.processing_start_time<time_difference)
        )
    print("hello")
    TempProxy = session.execute(query)

    add=""

    fetchCount = 0
    while(count != 5 and fetchCount < 2):
        fetchCount = fetchCount + 1
        add=fetchNext(TempProxy)
        address.clear()
        ids = []
        for a in add:
            address.append(a[0])
            ids.append(a[1])
            data["address"][a[1]] = {}
            data["address"][a[1]]["address"] = a[0]
            data["address"][a[1]]["pincode"] = a[2]
            data["address"][a[1]]["country"] = "th"
        # print('3')
        result = normalParse(data)
        # print('2')
        for id in ids:
        # print("New parsed address status and id", secondResult[id]["RelationshipCheck"], secondResult[id], )
          if(result[id]["RelationshipCheck"]):
             count+=1
             idList.append(id)
             returnResult.append(result[id])
          if(count==5):
             break
    # idList=[1,2]
    # print(idList)
    if (len(idList)==0): return []

    stmt = (
        update(NonLabeledAddress)
        .where(NonLabeledAddress.address_id.in_(idList))
        .where(NonLabeledAddress.company_id==company_id)
        .where(NonLabeledAddress.user_id==user_id)
        .values(processing_start_time=datetime.now())
    )
    session.execute(stmt)
    session.commit()

    # print("Count = ", count)
    return returnResult

def parseAddress(addr,company_id,country_code):
    print(ThaiParser.parse("บ้านเลข40/4ซอยรัชดาภิเษก32แยก7แขวงจันทรเกษมเขตจตุจักรกรุงเทพ10900, 10900, จตุจักร/ Chatuchak, กรุงเทพมหานคร/ Bangkok"))

def getTable(name):
    if(name=='al1'):
        return AL1, AL1.syn, AL1.al1
    elif(name=='al2'):
        return AL2, AL2.syn, AL2.al2
    elif(name=='al3'):
        return AL3, AL3.syn, AL3.al3
    elif(name=='sort_code'):
        return SortCodeMaster, None, SortCodeMaster.sort_code

def enhance(addEnhance, company_id):
    for item in addEnhance:
        obj, synList, key = getTable(item[0])
        syn = (session.query(synList).where(key==item[1]).first())[0]

        if(len(syn)==0):
            curr = obj()
            curr.make([item[1], item[2], company_id])
            session.add(curr)
        else:
            dic = syn.split(',')
            found = False
            for word in dic:
                if(word==item[2]):
                    found=True
                    break
            if(not found):
                syn = syn + ',' + item[2]
                session.execute(update(obj).where(key==item[1]).values(syn=syn))

def addNew(addition, pincode, company_id):
    for item in addition:
        obj, synList, key = getTable(item[0])
        values=[]
        if(item[0]=='sort_code'):
            values = session.query(key).filter_by(pincode=pincode).all()
        else:
            values = session.query(key).all()

        print(values)
        found = False
        for v in values:
            if(v[0]==item[1]):
                found=True
                break
        
        # print(found)

        if(not found):
            curr = obj()
            if(item[0]=='sort_code'):
                curr.createObject([0, pincode, item[1], company_id, datetime.now()])
            else:
                curr.make([item[1], item[1], company_id])

            session.add(curr)

def addSyn(addresses, company_id, user_id):
    for add in addresses:
        add['user_id']=user_id
        add['company_id']=company_id

        enhance(add["enhance"], company_id)
        addNew(add['addNew'], add['pincode'], company_id)
            # print(syn)
        
    session.commit()
    return addresses

