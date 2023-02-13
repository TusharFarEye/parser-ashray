from .parser.thaiParser import ThaiParser
from .parser.thaiParser import SynonymFilter
from service.Connections import *
from models.AlMaster import *
from models.SortCodeMaster import *
from service.AddressService import *
import requests
import asyncio
from datetime import datetime
import aiohttp
from string import Template
from service.parser.thaiParser.ThaiParser import helper

headers = {
    'Content-Type': 'application/json',
}

def get_parser(parserName):
    if parserName == "thaiParser":
        thaiParser = ThaiParser
        return thaiParser
    elif parserName == "spanishParser":
        pass
    else:
        pass

priority = ['pincode','al3','al2']


def normalParse(data):
    start = datetime.now()
    parser = get_parser(data["parserName"])
    # print("data[parserName] = ", data["parserName"][0])
    parsed_address = {}

    tasks=[]
    for k in data["address"]:
        d = data["address"][k]
        tasks.append(parser.parse(d["address"],d["pincode"]))
    
    # print('1')
    parsed_addr = asyncio.run(parser.helper(tasks))
    # print('2')
    i=0
    for k in data["address"]:
        d = data["address"][k]
        parsed_address[k] = { 'parsed_address': parsed_addr[i], 'address': d["address"], 'pincode': d["pincode"], 'country': d['country'] }
        i+=1
    
    end = datetime.now()
    relationshipCheckNew(parsed_address)

    return parsed_address

def relationshipCheck(parsedAddress):
    print(parsedAddress)
    for k in parsedAddress:
        d = parsedAddress[k]
        alRels = None
        for i in priority:

            if i in d:
                # print(i + " Entered")
                val2 = None
                # if i == "sort_code" and "pincode" in d:
                #     val2 = d["pincode"]
                alRels = getRelations(i,d[i],val2,1,'th')
                break
                # if rel is None:
                #     continue
        alRelArr = []
        for i in alRels:
            found = True
            if ('al1' in d["parsed_address"] and len(d["parsed_address"]['al1']) != 0 and d["parsed_address"]['al1'][0] != i["al1"]) or ('al1Syn' in d["parsed_address"] and len(d["parsed_address"]['al1Syn']) != 0 and d["parsed_address"]['al1Syn'][0] != i["al1"]):
                found = False
            if ('al2' in d["parsed_address"] and len(d["parsed_address"]['al2']) != 0 and d["parsed_address"]['al2'][0] != i["al2"]) or ('al2Syn' in d["parsed_address"] and len(d["parsed_address"]['al2Syn']) != 0 and  d["parsed_address"]['al2Syn'][0] != i["al2"]):
                found = False
            if ('al3' in d["parsed_address"] and len(d["parsed_address"]['al3']) != 0 and d["parsed_address"]['al3'][0] != i["al3"]) or ('al3Syn' in d["parsed_address"] and len(d["parsed_address"]['al3Syn']) != 0 and d["parsed_address"]['al3Syn'][0] != i["al3"]):
                found = False
            if found:
                alRelArr.append(i)

        if len(alRelArr) == 0:
            d["RelationshipCheck"] = False
        else:
            d["RelationshipCheck"] = True
        pincodes = []
        for i in alRelArr:
            if i["pincode"] != '' or i["pincode"] is not None:
                pincodes.append(i["pincode"])
        d['sortCodeRelCheck'] = 'NA'
        # alRelArrRes = alRelArr
        if 'sort_code' in d:
            sortCodePincodes = getRelations('sort_code', d["sort_code"],pincodes,1,'th')
            if len(sortCodePincodes) == 0:
                d['sortCodeRelCheck'] = 'Failed'
            else:
                d['sortCodeRelCheck'] = 'Success'
        


def getRelations(levelName, value, value2, companyId, countryCode):
    curr = conn.cursor()
    if levelName == 'sort_code':
        pincodesString = "("
        first = True
        for i in value2:
            if first:
                pincodesString = pincodesString + "'"+str(i)+"'"
            else:
                pincodesString = pincodesString + ",'"+str(i)+"'"
        pincodesString += ")"

        query = "Select * from sort_code_master where pincode in {0} and company_id ={1} and sort_code={2}".format(pincodesString,companyId,value)
        curr.execute(query)
        res = curr.fetchall()
        ret = createSortCodeMasterFromArray(res)
        pincodes = []
        for i in ret:
            pincodes.append(i.pincode)
        return pincodes
    elif levelName == 'keyword':
        pass
    else:
        # query = "Select * from al_master where company_id ='{0}' and country_code = '{1}' and {2} = '{3}'".format(
        #     companyId, countryCode,levelName, value)
        # curr.execute(query)
        # res = curr.fetchall()
        # ret = createAlmasterFromArray(res)

        ret = getAlMaster(value,levelName)

        # for row in res:
        #     print("ID = ", row[0])
        #     print("NAME = ", row[1])
        #     print("ADDRESS = ", row[2])
        #     print("SALARY = ", row[3], "\n")
        return ret
        # print(res)
        #
        # if (len(res) == 0): return None
        # return res

# def countValidRelation(rel,)
def similarValues(data):
    possibleNonAlLevel = ['sort_code','keyword']
    if data is not None and data["levelName"] in possibleNonAlLevel:
        return asyncio.run(similarHelper(data['value'], data['pincode'], data['levelName']))

async def similarHelper(value, pincode, levelName):
    return await SynonymFilter.getSimilarText(value, pincode, levelName)

def getAlMaster(text,levelName):
    r = requests.get('http://es-data-team-office.k8s.fareye.io/al_master/_search?pretty',

    headers = {'Content-type': 'application/json'},

    json = {
        "query": {
            "bool": {
                "filter": [{
                    "term": {
                        levelName: text
                    }
                }]
            }
        }
    })
    
    if(r.status!=200):
        return []

    parsed = r.json()
    # print(parsed)
    lst = parsed['hits']['hits']
    # print(lst)
    if len(lst) == 0:
        return []

    arr = []
    for i in lst:
        val = i['_source']
        arr.append(val)
        # print(val["esid"])
    return arr

def alsByPincode(pincode, al1, al2, al3):
    r = requests.get(esUrl+'al_master/_search?pretty', headers = headers, 
    json = {
        "query": {
            "bool": {
                "filter": {
                    "term": {
                        "pincode": pincode
                    }
                }
            }
        }
    })

    finalAl1=''
    finalAl2=''
    finalAl3=''
    
    if(len(al1)>0):
        finalAl1 = next(iter(al1))
    if(len(al2)>0):
        finalAl2 = next(iter(al2))
    if(len(al3)>0):
        finalAl3 = next(iter(al3))

    if(r.status!=200):
        return finalAl1, finalAl2, finalAl3, False

    parsed = r.json()
    lst = parsed['hits']['hits']
    maxScore = 0
    
    if len(lst)==0:
        return finalAl1, finalAl2, finalAl3, False
    for entry in lst:
        score=0
        if(entry['_source']['al1'] in al1):
            score+=1
        if(entry['_source']['al2'] in al2):
            score+=1
        if(entry['_source']['al3'] in al3):
            score+=1
        
        if(score>maxScore):
            score=maxScore
            finalAl1, finalAl2, finalAl3 = entry['_source']['al1'], entry['_source']['al2'], entry['_source']['al3']

    return finalAl1, finalAl2, finalAl3, True

def clash(address, s1, s2):
    start1 = address.find(s1)
    end1 = start1+len(s1)-1

    start2 = address.find(s2)
    end2 = start2+len(s2)-1

    if((start1<=start2 and end1>=start2) or (start2<=start1 and end2>=start1)):
        return True
    
    return False

async def check(add):
    al1=set(add['parsed_address']['al1'])
    al2=set(add['parsed_address']['al2'])
    al3=set(add['parsed_address']['al3'])

    removeAl1 = set()
    removeAl2 = set()

    for a1 in al1:
        for a2 in al2:
            if(clash(add['address'], a1, a2)):
                removeAl1.add(a1)
    
    for a1 in al1:
        for a3 in al3:
            if(clash(add['address'], a1, a3)):
                removeAl1.add(a1)
    
    for a2 in al2:
        for a3 in al3:
            if(clash(add['address'], a2, a3)):
                removeAl2.add(a2)
    
    for i in removeAl1:
        al1.remove(i)

    for j in removeAl2:
        al2.remove(j)
    

    add['parsed_address']['al1'], add['parsed_address']['al2'], add['parsed_address']['al3'] , add['RelationshipCheck']= alsByPincode(add['pincode'], al1, al2, al3)


def relationshipCheckNew(parsedAddress):
    tasks=[]
    
    for k in parsedAddress:
        add = parsedAddress[k]
        tasks.append(check(add))

    asyncio.run(helper(tasks))
        # alsByPincode(add['pincode'], al1, al2, al3)
