from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import UniqueConstraint
# from sqlalchemy.orm import relationship
# from models.AlMaster import AlMaster

baseKeyWords = declarative_base()

class KeyWord(baseKeyWords):

    __tablename__ = 'keyword_master'

    id = Column(Integer, primary_key=True)
    # al_id = Column(Integer, ForeignKey('al_master.id'))
    sc_id = Column(Integer)
    keyword = Column(String)
    keyword_syn = Column(String)
    company_id = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False)
    UniqueConstraint(keyword)
    # al_master = relationship(AlMaster)

'''id serial not null PRIMARY KEY not null,
   al_id int,
   sc_id int,
   keyword text,
   company_id int,
   created_at TIMESTAMP NOT NULL,
   UNIQUE(al_id,keyword),
   FOREIGN KEY(al_id)
   REFERENCES al_master(id)
'''