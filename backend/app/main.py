from fastapi import FastAPI
from app.routers import profiles
from app.database import engine
from app.models import Base

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(profiles.router)

@app.get('/')
def read_root():
    return {"hello": "world"}
