__author__ = 'Paolo Bellagente'


#  Documentation for this module.
#
#  More details.

################################## DATABASE ##############################################

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

## Database name
db_name = "testDatabase"
## Database user
db_uid = "root"
## Database user's password
db_passwd = ""
## Database host
db_host = "localhost"
##
# set the database connection engine
engine = create_engine('mysql+pymysql://'+db_uid+':'+db_passwd+'@'+db_host+'/'+db_name)

## Classe base per l'ereditarieta' delle tabelle
#
# Permette di istanziare una volta la classe base e riutilizzarla
Base = declarative_base()

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(INTEGER, primary_key=True)
    semesterStartDate = Column(DATE)
    semesterEndDate = Column(DATE)
    # lesson's start hour
    hour = Column(TIME)
    # lesson's day of the week coded form 0 to 6 where 0 is monday and 6 is sunday.
    day = Column(INTEGER)
    subject = Column(VARCHAR(200))
    rooms = Column(VARCHAR(30))
    address = Column(VARCHAR(50))
    teacher = Column(VARCHAR(50))

    def __init__(self):
        self.teacher = ''

    # persist the entity into the database
    def persist(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(self)
        session.commit()
        session.close()


# todo: create new entity here

## Create the necesary tables into the databse
Base.metadata.create_all(engine)

