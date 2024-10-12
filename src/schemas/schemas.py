from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
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
    start_date = Column(String, default=lambda: str(datetime.now(timezone.utc).date()))
    end_date = Column(String, default=lambda: str(datetime.now(timezone.utc).date()))
    reminder_sent = Column(Boolean, default=False)  
    reminder_time = Column(String, default=lambda: str(datetime.now(timezone.utc).date()))    

    user  = relationship("Users")


def create_default_roles(db):
    admin_role = db.query(Role).filter(Role.role_name == 'Admin').first()
    user_role = db.query(Role).filter(Role.role_name == 'User').first()
    
    if not admin_role:
        new_admin_role = Role(role_name='Admin')
        db.add(new_admin_role)
    
    if not user_role:
        new_user_role = Role(role_name='User')
        db.add(new_user_role)

    db.commit()