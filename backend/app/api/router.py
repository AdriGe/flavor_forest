from fastapi import APIRouter
from api.user_routes import router as user_router
from api.food_routes import router as food_router
from api.portion_routes import router as portion_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(food_router, prefix="/foods", tags=["foods"])
api_router.include_router(portion_router, prefix="/foods", tags=["portions"])
