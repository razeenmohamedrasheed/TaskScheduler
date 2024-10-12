import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  
from src.db import get_db
from src.models import Base  
from src.schemas import schemas

# Setup the test database
DATABASE_URL = "sqlite:///../taskmanager.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database schema
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Create a test client
client = TestClient(app)

# Sample user for authentication (mocking the get_current_user dependency)
mock_user = {
    "user": {
        "userid": 1,
        "role_id": 1,
        "email": "test@example.com"
    }
}

# Mocking the get_current_user dependency
@pytest.fixture
def override_current_user():
    with patch("src.utility.auth.get_current_user") as mock:
        mock.return_value = mock_user
        yield mock

@pytest.mark.asyncio
async def test_create_task(override_current_user):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "A task for testing.",
        "start_date": "2024-10-12",
        "end_date": "2024-10-13",
        "reminder_time": "2024-10-11T10:00:00",
        "reminder_sent": False,
        "user_id": 1
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Task created successfully", "task_id": 1}

@pytest.mark.asyncio
async def test_list_all_tasks(override_current_user):
    client.post("/tasks", json={
        "title": "Test Task",
        "description": "A task for testing.",
        "start_date": "2024-10-12",
        "end_date": "2024-10-13",
        "reminder_time": "2024-10-11T10:00:00",
        "reminder_sent": False,
        "user_id": 1
    })
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_update_task(override_current_user):
   
    client.post("/tasks", json={
        "title": "Test Task",
        "description": "A task for testing.",
        "start_date": "2024-10-12",
        "end_date": "2024-10-13",
        "reminder_time": "2024-10-11T10:00:00",
        "reminder_sent": False,
        "user_id": 1
    })


    response = client.put("/tasks/1", json={
        "title": "Updated Task",
        "description": "Updated description."
    })
    assert response.status_code == 202
    assert response.json()["message"] == "Task updated successfully"

@pytest.mark.asyncio
async def test_delete_task(override_current_user):

    client.post("/tasks", json={
        "title": "Test Task",
        "description": "A task for testing.",
        "start_date": "2024-10-12",
        "end_date": "2024-10-13",
        "reminder_time": "2024-10-11T10:00:00",
        "reminder_sent": False,
        "user_id": 1
    })

    response = client.delete("/tasks/1")
    assert response.status_code == 202
    assert response.json() == {"message": "Task deleted successfully", "task_id": 1}

@pytest.mark.asyncio
async def test_get_individual_tasks(override_current_user):

    client.post("/tasks", json={
        "title": "Test Task",
        "description": "A task for testing.",
        "start_date": "2024-10-12",
        "end_date": "2024-10-13",
        "reminder_time": "2024-10-11T10:00:00",
        "reminder_sent": False,
        "user_id": 1
    })

    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
