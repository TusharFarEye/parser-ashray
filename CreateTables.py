from service.Connections import *
from models.NonLabeledAddress import baseNonLableAdd
from models.HubPincodeMapping import baseHubPin
from models.SortCodeMaster import baseSortCode
from models.AL1 import baseAl1
from models.AL2 import baseAl2
from models.AL3 import baseAl3
from models.SortCodeMaster import baseSortCode
from models.KeyWord import baseKeyWords
from models.AlMaster import baseAlMaster

# from models.TempraryTable import baseTemp, Number

baseAlMaster.metadata.create_all(db)
baseNonLableAdd.metadata.create_all(db)
baseHubPin.metadata.create_all(db)
baseAl1.metadata.create_all(db)
baseAl2.metadata.create_all(db)
baseAl3.metadata.create_all(db)
baseSortCode.metadata.create_all(db)
baseKeyWords.metadata.create_all(db)

# baseTemp.metadata.create_all(db)

# Create 
# for i in range(20):
#     temp = Number(id=i)
#     session.add(temp)  
#     session.commit()

# # Read
# films = session.query(Film)  
# for film in films:  
#     print(film.title)

# # Update
# doctor_strange.title = "Some2016Film"  
# session.commit()

# # Delete
# session.delete(doctor_strange)  
# session.commit()  