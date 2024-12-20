from fastapi import FastAPI
from app.routers import profiles
from app.database import engine, Base

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def read_root():
    return {"hello": "world"}
