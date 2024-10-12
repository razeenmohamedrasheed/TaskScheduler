import smtplib
from fastapi import APIRouter,status,HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from src.models.task_models import task,updatetask
from typing import List
from fastapi.params import Depends
from src.db import get_db,SessionLocal,engine
from src.schemas import schemas
from src.utility.auth import get_current_user 
from datetime import date,datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


router = APIRouter(
    tags=["Manage Tasks"]
)

schemas.Base.metadata.create_all(bind=engine)


async def send_reminder_email(task, current_user):
    print(current_user)
    print(task.title) 
    print(task.end_date) 
    
    # Email configuration
    sender_email = ''  # Your email address
    sender_password = ''  # Your email password
    recipient_email = current_user['email']  # Recipient's email address

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = f'Reminder: Task {task.title} is due soon!'

    # Email body
    body = f"Hello {current_user['user']}, just a reminder that your task '{task.title}' is due on {task.end_date}."
    message.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password) 
            server.sendmail(sender_email, recipient_email, message.as_string()) 
            print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

@router.get('/tasks',status_code=status.HTTP_200_OK)
async def listAlltasks(db:Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role_id"] != 1:
            raise HTTPException(status_code=403, detail="Only Admin can view this ")

        tasks = db.query(schemas.Task).all()
        return tasks
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Error")

@router.post('/tasks',status_code=status.HTTP_201_CREATED)
async def createTask(payload:task,background_tasks: BackgroundTasks, db:Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
   
   try:
        if current_user["role_id"] != 1:
            # Ensure the user can only create tasks for themselves
            if payload.user_id != current_user["user"].userid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create tasks for other users.")
            # Assign the current user's ID to the task's user_id if they are not an admin
            payload.user_id = current_user["user"].userid

      
        start_date = datetime.strptime(payload.start_date, "%Y-%m-%d") if isinstance(payload.start_date, str) else payload.start_date
        end_date = datetime.strptime(payload.end_date, "%Y-%m-%d") if isinstance(payload.end_date, str) else payload.end_date
        reminder_time = datetime.strptime(payload.reminder_time, "%Y-%m-%dT%H:%M:%S") if isinstance(payload.reminder_time, str) else payload.reminder_time
        
        new_task = schemas.Task(
            user_id=payload.user_id,
            title=payload.title,
            description=payload.description,
            start_date=start_date,
            end_date=end_date,
            reminder_sent=payload.reminder_sent, 
            reminder_time=reminder_time
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        background_tasks.add_task(send_reminder_email, new_task, current_user)
        
        return {
            "message": "Task created successfully",
            "task_id": new_task.taskid
        }

   except HTTPException as http_exc:
        raise http_exc
   except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the task.")
   

@router.get('/tasks/{user_id}', status_code=status.HTTP_200_OK)
async def lisIndividualTasks(user_id:int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user) ):
    try:
        tasks = db.query(schemas.Task).filter(schemas.Task.user_id == user_id).all()

        if not tasks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found for this user.")
 
        if current_user["role_id"] != 1 and user_id != current_user["user"].userid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view these tasks.")
        return tasks
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Occured")


@router.put('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: int,payload:updatetask, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
        try:
            task = db.query(schemas.Task).filter(schemas.Task.taskid == task_id).first()
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            
            if current_user["role_id"] != 1 and task.user_id != current_user["user"].userid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create  task for this user.")

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
        except HTTPException as http_exc:
            raise http_exc
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
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the task.")
