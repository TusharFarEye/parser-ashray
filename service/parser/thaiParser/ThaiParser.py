from .data import districtSet,provinceSet,tambonSet
from attacut import tokenize
import asyncio
from datetime import datetime

from .SynonymFilter import getSynonym, getSimilarText, getAlSynonym

district = districtSet.district
province = provinceSet.province
tambon = tambonSet.tambon
def tokengen(addr):
  words = tokenize(addr)
  wordsNew = []
  k = 0
  skip = False
  for i in words:
    if skip:
      skip = False
      continue
    l = len(i)
    if l > 1 or i[0].isalnum():
      wordsNew.append(i) 
    if i == '/' and k > 0 and k < len(words)-2 and words[k-1].isnumeric() and words[k+1].isnumeric():
      wordsNew.pop()
      wordsNew.append(words[k-1]+i+words[k+1]) 
      skip = True
    k=k+1
  return wordsNew

async def parse(add,pincode):
  # start = datetime.now()
  # print(start)
  tambonList = []
  provinceList = []
  districtList = []
  sortCode = ""
  # keyWord = ""

  sortCodeArr = []
  keywordArr = []
#   possibleTambon = set()
#   possibleDistrict = set()
  words2 = tokenize(add)
  for i in words2:
    if i in province:
      provinceList.append(i)
    if i in district:
      districtList.append(i)
    if i in tambon:
      tambonList.append(i)
  
  # print(provinceList, districtList, tambonList)
  # tasks=[]
  
  tasks = [getSimilarText(add,pincode,"sort_code"), getSimilarText(add,pincode,"keyword")]
  sortCodeArr, keywordArr = await helper(tasks)

  # print(keywordArr)
  # tasks = [getAlSynonym(add,"al1"), getAlSynonym(add,"al2"), getAlSynonym(add,"al3"), getSimilarText(add,pincode,"sort_code"), getSimilarText(add,pincode,"keyword")]
  # provinceSynonymsList, districtSynonymsList, tambonSynonymsList, sortCodeArr, keywordArr = asyncio.run(helper(tasks))

  # if len(provinceList) == 0 or len(districtList) == 0 or len(tambonList) == 0:
    # retArr = getSynonym(add)
    # tasks = [getAlSynonym(add,"al1"), getAlSynonym(add,"al2"), getAlSynonym(add,"al3")]
    # provinceSynonymsList, districtSynonymsList, tambonSynonymsList, sortCodeArr, keywordArr = asyncio.run(helper(tasks))
  
    # provinceSynonymsList = getAlSynonym(add,"al1")
    # districtSynonymsList = getAlSynonym(add,"al2")
    # tambonSynonymsList = getAlSynonym(add,"al3")
    # for j in retArr:
    #   if j in province:
    #     provinceSynonymsList.append(j)
    #   elif j in district:
    #     districtSynonymsList.append(j)
    #   elif j in tambon:
    #     tambonSynonymsList.append(j)

  # provinceSynonymsList = getAlSynonym(add,"al1")
  # districtSynonymsList = getAlSynonym(add,"al2")
  # tambonSynonymsList = getAlSynonym(add,"al3")

  # sortCodeArr = getSimilarText(add,pincode,"sort_code")
  # keywordArr = getSimilarText(add,pincode,"keyword")
  
  if len(sortCodeArr) != 0:
    sortCode = sortCodeArr[0]
  # if len(keywordArr) != 0:
  #   keyWord = keywordArr[0]
  end = datetime.now()
  # print(end-start)
  return {"al3": tambonList,"al1": provinceList,"al2": districtList , "sort_code": sortCode , "keyword": keywordArr, "pincode": pincode }

async def helper(tasks):
  v = await asyncio.gather(*tasks)
  # print(v)
  return v

# print(parser("49/190 หมู่7, 12120, คลองหลวง/ Khlong Luang, ปทุมธานี/ Pathum Thani ปทุมธานี/ Pathum Thani 12120"))
# print(tokengen("7/31 ม.7 ต.คลองสอง อ.คลองหลวง ร้านค้า, 12120, คลองหลวง/ Khlong Luang, ปทุมธานี/ Pathum Thani"))
# add = "บ้านเลข40/4ซอยรัชดาภิเษก32แยก7แขวงจันทรเกษมเขตจตุจักรกรุงเทพ10900, 10900, จตุจักร/ Chatuchak, กรุงเทพมหานคร/ Bangkok"
# print(parse(add,'10900'))
