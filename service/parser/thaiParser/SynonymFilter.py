# from elasticsearch import Elasticsearch
import pandas as pd
import requests
import json
from service.Connections import *
import aiohttp
from datetime import datetime

def getSynonym(text):
    r = requests.get(esUrl+'synonym_test/_search?pretty',

    headers = {'Content-type': 'application/json'},

    json = {
        "query": {
            "bool": {
                "must": [
                    { "match": { "some_text": text } }
                ]
            }
        }
        }
    )
    if(r.status!=200):
        return []

    parsed = r.json()
    lst = parsed['hits']['hits']
    if len(lst) == 0:
        return []

    arr = []
    for i in lst:
        arr.append(i['_source']['some_text'])
    return arr



async def getSimilarText(text,pincode,textKey):
    # print("inside similar", datetime.now())
    async with aiohttp.ClientSession() as session:
        async with session.get(
        esUrl+textKey+'_master/_search?pretty',
        headers = {'Content-type': 'application/json'},

        json = {
            "query": {
                "bool": {
                    "must": [
                        { "match": { textKey: text } }
                    ],
                    "filter": [{
                        "term": {
                            "pincode": pincode
                        }
                        }
                    ]
                }
            }
            }
        ) as r:
            if(r.status!=200):
                return []

            parsed = await r.json() 
            
            lst = parsed['hits']['hits']
            if len(lst) == 0:
                return []
            resArr = []
            k= 0
            for i in lst:
                if k == 5:
                    break
                k = k + 1
                resArr.append(i['_source'][textKey])
            # print(textKey, resArr)
            return resArr

async def getAlSynonym(text,levelName):
    # print("inside synonym", datetime.now())
    async with aiohttp.ClientSession() as session:

        async with session.get('http://es-data-team-office.k8s.fareye.io/al_master/_search?pretty',

        headers = {'Content-type': 'application/json'},

        json = {
            "query": {
                "bool": {
                    "must": [
                        { "match": { levelName: text } }
                    ]
                }
            }
            }
        ) as r:
            if(r.status!=200):
                return []

            parsed = await r.json()
            lst = parsed['hits']['hits']
            if len(lst) == 0:
                return []

            arr = []
            repeat = set()
            for i in lst:
                val = i['_source'][levelName]
                if val not in repeat:
                    repeat.add(val)
                    arr.append(val)
            return arr