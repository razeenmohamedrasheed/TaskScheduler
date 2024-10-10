from fastapi import APIRouter,status,HTTPException
from src.models.task_models import task

router = APIRouter(
    tags=["Manage Tasks"]
)


@router.get('/tasks',status_code=status.HTTP_200_OK)
async def listAlltasks():
    return {
        "message":'success',
    }

@router.post('/tasks',status_code=status.HTTP_201_CREATED)
async def listAlltasks(payload:task):
    return {
        "message":'success',
        "data": payload
    }


@router.put('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id: int):
        return {
            "message": 'Task updated successfully',
            "data": task_id
        }

@router.delete('/tasks/{task_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_task(task_id: int):
     return {
            "message": 'Task updated successfully',
            "data": task_id
        }