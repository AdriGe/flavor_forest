# main.py ou dans un fichier approprié dans votre dossier api
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from models.foods import Food
from models.portions import Portion
from schemas.foods import FoodCreate, FoodResponse, FoodUpdate, FoodListResponse, FoodDetail
from schemas.portions import PortionDetail
from dependencies import get_db, SessionLocal, model_to_dict
from typing import Optional
import unidecode
import uuid
from api.user_routes import get_current_user
from models.user import User

router = APIRouter()

def cast_food_to_food_details(food: Food) -> FoodDetail:
    casted_food = FoodDetail(
        food_id=food.food_id,
        name=food.name,
        brand=food.brand,
        kcal=food.kcal,
        fat=food.fat,
        saturated_fat=food.saturated_fat,
        carbohydrate=food.carbohydrate,
        sugars=food.sugars,
        fiber=food.fiber,
        protein=food.protein,
        sodium=food.sodium,
        unit_id=food.unit_id,
        portions=[PortionDetail(**model_to_dict(portion)) for portion in food.portions]
    )

    return casted_food


@router.get("", response_model=FoodListResponse)
def get_foods(
    name: Optional[str] = None,
    brand: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")

    query = db.query(Food)

    if name:
        for word in name.split():
            normalized_word = unidecode.unidecode(word)  # Normalisation des accents
            query = query.filter(func.lower(Food.name).ilike(f"%{normalized_word.lower()}%"))
    if brand:
        normalized_brand = unidecode.unidecode(brand)
        query = query.filter(func.lower(Food.brand).ilike(f"%{normalized_brand.lower()}%"))

    total_foods = query.count()
    foods = query.offset((page - 1) * page_size).limit(page_size).all()
    foods_casted = [cast_food_to_food_details(new_food) for new_food in foods]

    return FoodListResponse(
        total_foods=total_foods,
        total_pages=(total_foods + page_size - 1) // page_size,
        foods=foods_casted
    )


@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: uuid.UUID, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_food = db.query(Food).filter(Food.food_id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food


@router.post("", response_model=FoodResponse)
async def create_food(
    food: FoodCreate, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        new_food = Food(
            user_id=food.user_id,
            name=food.name,
            brand=food.brand,
            kcal=food.kcal,
            fat=food.fat,
            saturated_fat=food.saturated_fat,
            carbohydrate=food.carbohydrate,
            sugars=food.sugars,
            fiber=food.fiber,
            protein=food.protein,
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
async def update_food(
    food_id: uuid.UUID, 
    food_data: FoodUpdate, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_food = db.query(Food).filter(Food.food_id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

    # Mise à jour des champs de l'aliment, en ignorant les portions
    food_attrs = {k: v for k, v in vars(food_data).items() if v is not None and k != 'portions'}
    for var, value in food_attrs.items():
        setattr(db_food, var, value)

    # Mise à jour des portions associées
    if food_data.portions is not None:
        for portion_data in food_data.portions:
            # Recherchez une portion existante ou créez-en une nouvelle
            db_portion = db.query(Portion).filter(Portion.food_id == food_id, Portion.name == portion_data.name).first()
            if not db_portion:
                db_portion = Portion(food_id=food_id, **portion_data.dict())
                db.add(db_portion)
            else:
                for var, value in vars(portion_data).items():
                    setattr(db_portion, var, value)


    db.commit()
    db.refresh(db_food)
    return db_food
