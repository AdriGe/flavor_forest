# main.py ou dans un fichier approprié dans votre dossier api
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from models.foods import Food
from models.portions import Portion
from schemas.portions import PortionCreate, PortionUpdate, PortionResponse
from dependencies import get_db

router = APIRouter()

@router.post("/{food_id}/portions", response_model=PortionResponse)
async def add_portion(food_id: int, portion_data: PortionCreate, db: Session = Depends(get_db)):
    # Vérifiez d'abord si l'aliment existe
    food = db.query(Food).filter(Food.food_id == food_id).first()
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

    # Créer et ajouter la nouvelle portion
    new_portion = Portion(food_id=food_id, name=portion_data.name, size=portion_data.size)
    db.add(new_portion)
    db.commit()
    db.refresh(new_portion)

    return new_portion


@router.put("/{food_id}/portions/{portion_id}", response_model=PortionResponse)
async def update_portion(food_id: int, portion_id: int, portion_data: PortionUpdate, db: Session = Depends(get_db)):
    db_portion = db.query(Portion).filter(Portion.food_id == food_id, Portion.portion_id == portion_id).first()
    if not db_portion:
        raise HTTPException(status_code=404, detail="Portion not found")

    # Mise à jour explicite des champs
    if portion_data.name is not None:
        db_portion.name = portion_data.name
    if portion_data.size is not None:
        db_portion.size = portion_data.size

    db.commit()
    db.refresh(db_portion)
    return db_portion


@router.delete("/{food_id}/portions/{portion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portion(food_id: int, portion_id: int, db: Session = Depends(get_db)):
    db.query(Portion).filter(Portion.food_id == food_id, Portion.portion_id == portion_id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)