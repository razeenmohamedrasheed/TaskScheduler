from pydantic import BaseModel
from typing import Optional

class task(BaseModel): 
    user_id :int
    title :str
    description :str
    start_date :str
    end_date :str

class updatetask(BaseModel): 
    user_id :int
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
