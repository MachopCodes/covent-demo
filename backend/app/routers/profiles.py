from fastapi import APIRouter

router = APIRouter()

@router.get("/profiles")
async def get_profiles():
    return {"message": "Profiles endpoint is working!"}
