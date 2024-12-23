from fastapi import FastAPI
from app.routers import sponsors, users, events
from app.database import engine
from app.models import Base

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sponsors.router)
app.include_router(users.router)
app.include_router(events.router)

@app.get('/')
def read_root():
    return {"hello": "world"}
