import sqlite3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Administrator(Base):
    __tablename__="Administrator"
    AdministratorID = Column(Integer, primary_key = True, autoincrement = True)
    Name = Column(String)
    Surname = Column(String)
    Email = Column(String)
    Password = Column(String)