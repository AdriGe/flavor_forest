# main.py ou dans un fichier approprié dans votre dossier api
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.exc import IntegrityError
from models.foods import Food
from models.portions import Portion
from schemas.foods import FoodCreate, FoodResponse, FoodUpdate
from dependencies import get_db, SessionLocal

router = APIRouter()

@router.post("", response_model=FoodCreate)
async def create_food(food: FoodCreate, db: SessionLocal = Depends(get_db)):
    try:
        new_food = Food(
            user_id=food.user_id,
            name=food.name,
            brand=food.brand,
            calories=food.calories,
            fats=food.fats,
            saturated_fats=food.saturated_fats,
            carbohydrates=food.carbohydrates,
            sugars=food.sugars,
            fibers=food.fibers,
            proteins=food.proteins,
            sodium=food.sodium,
            unit_id=food.unit_id
        )

        if food.portions is not None:
            for portion_data in food.portions:
                db_portion = Portion(food_id=new_food.food_id, name=portion_data.name, size=portion_data.size)
                new_food.portions.append(db_portion)
                
        db.add(new_food)
        db.commit()
        db.refresh(new_food)
        return new_food
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id or other integrity issue")


@router.put("/{food_id}", response_model=FoodResponse)
async def update_food(food_id: int, food_data: FoodUpdate, db: SessionLocal = Depends(get_db)):
    db_food = db.query(Food).filter(Food.food_id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

    # Mise à jour des champs de l'aliment
    for var, value in vars(food_data).items():
        if value is not None:
            setattr(db_food, var, value)

    db.commit()
    db.refresh(db_food)
    return db_food


@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(food_id: int, db: SessionLocal = Depends(get_db)):
    db_food = db.query(Food).filter(Food.food_id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food
