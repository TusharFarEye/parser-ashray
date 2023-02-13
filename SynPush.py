from models.KeyWord import KeyWord
from models.SortCodeMaster import SortCodeMaster
from service.Connections import session
import requests
from datetime import datetime

keySyn = session.query(KeyWord.keyword_syn, KeyWord.keyword).all()
syn=[]
key=[]
for k in keySyn:
    syn.append(k[0])
    key.append(k[1])
print(syn, key)


def init():
    r = requests.put('http://localhost:9200/testing1/',
        headers = {'Content-type': 'application/json'},

        json = {
        "settings": {
            "analysis": {
            "analyzer": {
                "my_synonyms": {
                "tokenizer": "whitespace",
                    "filter": ["lowercase","my_synonym_filter"]
                    }
                },
            "filter": {
                "my_synonym_filter": {
                "type": "synonym",
                    "ignore_case": "true",
                    "synonyms": syn
                    }
                }
            }
        },

        "mappings" :{
        "properties": {
            "some_text": {
            "type": "text",
                "search_analyzer": "my_synonyms"
                }
            }
        }
        }
    )

    # print("index Status :" , r)
    return r


def addToDoc(text_id, text):
    r = requests.put(f"http://localhost:9200/testing1/_doc/{text_id}",
            headers = {'Content-type': 'application/json'},
            json = {
            "some_text": text
            }
        )
    # print("text added status", r)


def getSynonym(text):
    r = requests.get('http://localhost:9200/testing1/_search?pretty',

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

init()

for i in range(len(key)):
    addToDoc(i,key[i])

# print("get",getSynonym('Apple1'))
