from fastapi import APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from src.models.task_models import task,updatetask
from typing import List
from fastapi.params import Depends
from src.db import get_db,SessionLocal,engine
from src.schemas import schemas

router = APIRouter(
    tags=["Manage Tasks"]
)

schemas.Base.metadata.create_all(engine)

@router.get('/tasks',status_code=status.HTTP_200_OK)
async def listAlltasks():
    return {
        "message":'success',
    }

@router.post('/tasks',status_code=status.HTTP_201_CREATED)
async def createTask(payload:task,db:Session = Depends(get_db)):
    try:
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
            "message": "Created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the task.")

@router.get('/tasks/{user_id}', status_code=status.HTTP_200_OK)
async def lisIndividualTasks(user_id:int, db: Session = Depends(get_db)):
    try:
        tasks = db.query(schemas.Task).filter(schemas.Task.user_id == user_id).all()
        if not tasks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found for this user.")
        return tasks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Occured")


@router.put('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: int,payload:updatetask, db: Session = Depends(get_db)):
        try:
            task = db.query(schemas.Task).filter(schemas.Task.taskid == task_id).first()
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

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
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(schemas.Task).filter(schemas.Task.taskid == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
        db.delete(task)
        db.commit()

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the task.")