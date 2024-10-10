from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from src.db import Base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    taskid = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer) 
    title = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)