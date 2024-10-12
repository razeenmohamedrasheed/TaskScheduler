from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class task(BaseModel): 
    user_id :int
    title :str
    description :str
    start_date :date
    end_date :date
    reminder_sent: Optional[bool] = False  
    reminder_time: Optional[date] = None  

class updatetask(BaseModel): 
    user_id :int
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reminder_sent:Optional[bool] = None
