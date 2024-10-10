from fastapi import FastAPI
from src.routes import taskroutes
import uvicorn

app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "Welcome"} 


app.include_router(taskroutes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)