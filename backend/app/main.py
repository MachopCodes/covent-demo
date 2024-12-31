from fastapi import FastAPI
from app.routers import sponsors, users, events, auth, proposals
from app.database import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://covent-frontend.vercel.app"],  # Angular app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(sponsors.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(auth.router)
app.include_router(proposals.router)

@app.get('/')
def read_root():
    return {"hello": "world"}
