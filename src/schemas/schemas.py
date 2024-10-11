from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from src.db import Base,engine

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)

class Users(Base):
    __tablename__ = 'users'
    userid = Column(Integer,primary_key=True,index=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    username = Column(String)
    email = Column(String)
    contact = Column(String)
    password = Column(String)

    role = relationship("Role")

  
class Task(Base):
    __tablename__ = 'task'
    taskid = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.userid'), nullable=False) 
    title = Column(String)
    description = Column(String)
    start_date = Column(String, default=str(datetime.now(timezone.utc).date))
    end_date = Column(String, default=str(datetime.now(timezone.utc).date))

    user  = relationship("Users")
