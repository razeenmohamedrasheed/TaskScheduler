from fastapi import APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from src.models.task_models import task,updatetask
from typing import List
from fastapi.params import Depends
from src.db import get_db,SessionLocal,engine
from src.schemas import schemas
from src.utility.auth import get_current_user 

router = APIRouter(
    tags=["Manage Tasks"]
)

schemas.Base.metadata.create_all(bind=engine)

@router.get('/tasks',status_code=status.HTTP_200_OK)
async def listAlltasks(db:Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role_id"] != 1:
            raise HTTPException(status_code=403, detail="No Permission ")
        tasks = db.query(schemas.Task).all()
        return tasks
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No access to this API")

@router.post('/tasks',status_code=status.HTTP_201_CREATED)
async def createTask(payload:task,db:Session = Depends(get_db),current_user: dict = Depends(get_current_user) ):
   
   try:
        if current_user["role_id"] != 1:
            payload.user_id = current_user["user"].userid
        new_task = schemas.Task(
            user_id=payload.user_id,
            title=payload.title,
            description=payload.description,
            start_date=payload.start_date,
            end_date=payload.end_date
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return {
            "message": "Task created successfully",
            "task_id": new_task.taskid
        }

   except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the task.")
   

@router.get('/tasks/{user_id}', status_code=status.HTTP_200_OK)
async def lisIndividualTasks(user_id:int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user) ):
    try:
        tasks = db.query(schemas.Task).filter(schemas.Task.user_id == user_id).all()
        if not tasks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found for this user.")
          
        if current_user["role_id"] != 1 and task.user_id != current_user["user"].userid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have view the task.")
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Occured")


@router.put('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: int,payload:updatetask, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
        try:
            task = db.query(schemas.Task).filter(schemas.Task.taskid == task_id).first()
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            
            if current_user["role_id"] != 1 and task.user_id != current_user["user"].userid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this task.")

            task.title = payload.title if payload.title is not None or '' else task.title
            task.description = payload.description  if payload.title is not None or '' else task.description
            task.start_date = payload.start_date  if payload.title is not None or '' else task.start_date
            task.end_date = payload.end_date  if payload.title is not None or '' else task.end_date

            db.commit()
            db.refresh(task) 

            return {
                "message": "Task updated successfully",
                "data": task
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the task.")

@router.delete('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_task(task_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    try:
        task = db.query(schemas.Task).filter(schemas.Task.taskid == task_id).first()
        
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        print(current_user)
        if current_user["role_id"] != 1 and task.user_id != current_user["user"].userid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this task.")

        db.delete(task)
        db.commit()

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the task.")
