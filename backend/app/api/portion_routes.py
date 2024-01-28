# main.py ou dans un fichier approprié dans votre dossier api
from fastapi import APIRouter, HTTPException, Depends, status, Response
from models.foods import Food
from models.portions import Portion
from schemas.portions import PortionCreate, PortionUpdate, PortionResponse
from dependencies import get_db, SessionLocal
import uuid
from api.user_routes import get_current_user
from models.user import User

router = APIRouter()

@router.post("/{food_id}/portions", response_model=PortionResponse)
async def add_portion(
    food_id: uuid.UUID, 
    portion_data: PortionCreate, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifiez d'abord si l'aliment existe
    food = db.query(Food).filter(Food.food_id == food_id).first()
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

    # Vérifiez si une portion avec le même nom existe déjà pour cet aliment
    existing_portion = db.query(Portion).filter(Portion.food_id == food_id, Portion.name == portion_data.name).first()
    if existing_portion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Portion with this name already exists for this food")

    # Créer et ajouter la nouvelle portion
    new_portion = Portion(food_id=food_id, name=portion_data.name, size=portion_data.size)
    db.add(new_portion)
    db.commit()
    db.refresh(new_portion)

    return new_portion


@router.put("/{food_id}/portions/{portion_id}", response_model=PortionResponse)
async def update_portion(
    food_id: uuid.UUID, 
    portion_id: uuid.UUID, 
    portion_data: PortionUpdate, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_portion = db.query(Portion).filter(Portion.food_id == food_id, Portion.portion_id == portion_id).first()
    if not db_portion:
        raise HTTPException(status_code=404, detail="Portion not found")

    # Vérifiez si une portion avec le même nom existe déjà pour cet aliment
    existing_portion = db.query(Portion).filter(Portion.food_id == food_id, Portion.name == portion_data.name).first()
    if existing_portion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Portion with this name already exists for this food")

    # Mise à jour explicite des champs
    if portion_data.name is not None:
        db_portion.name = portion_data.name
    if portion_data.size is not None:
        db_portion.size = portion_data.size

    db.commit()
    db.refresh(db_portion)
    return db_portion


@router.delete("/{food_id}/portions/{portion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portion(
    food_id: uuid.UUID, 
    portion_id: uuid.UUID, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Portion).filter(Portion.food_id == food_id, Portion.portion_id == portion_id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)