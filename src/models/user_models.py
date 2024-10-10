from pydantic import BaseModel
from typing import Optional

class user(BaseModel): 
    role_id:int
    username:str
    email:str
    contact:str
    password:str