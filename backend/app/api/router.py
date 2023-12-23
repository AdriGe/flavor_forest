from fastapi import APIRouter
from api.user_routes import router as user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
