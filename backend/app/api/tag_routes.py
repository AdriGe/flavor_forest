from fastapi import APIRouter, HTTPException, Depends, status, Response
from models.tags import Tag, TagCategoryEnum
from schemas.tags import TagDetail, TagCreate, TagUpdate
from dependencies import get_db, SessionLocal
from sqlalchemy import and_
from typing import List
import uuid

router = APIRouter()

@router.get("", response_model=List[TagDetail])
def get_all_tags(db: SessionLocal = Depends(get_db)):
    # Récupérer tous les tags
    tags = db.query(Tag).all()
    
    # Convertir les tags en modèles Pydantic
    return [TagDetail(tag_id=tag.tag_id, name=tag.name, category=tag.category) for tag in tags]


@router.get("/{tag_id}", response_model=TagDetail)
def get_tag(tag_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    # Trouver le tag par son ID
    tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return TagDetail(tag_id=tag.tag_id, name=tag.name, category=tag.category)


@router.post("", response_model=TagDetail)
def create_tag(tag_data: TagCreate, db: SessionLocal = Depends(get_db)):
    # Vérifier si le tag existe déjà
    existing_tag = db.query(Tag).filter(and_(Tag.name == tag_data.name, Tag.category == tag_data.category)).first()

    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists"
        )

    # Créer le nouveau tag
    new_tag = Tag(
        name=tag_data.name,
        category=tag_data.category
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


@router.put("/{tag_id}", response_model=TagDetail)
def update_tag(tag_id: uuid.UUID, tag_data: TagUpdate, db: SessionLocal = Depends(get_db)):
    # Trouver le tag par son ID
    tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    # Vérifier si le nouveau nom de tag existe déjà
    existing_tag = db.query(Tag).filter(Tag.name == tag_data.name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )

    # Mettre à jour le tag
    tag.name = tag_data.name
    db.commit()

    return tag

@router.delete("/{tag_id}")
def delete_tag(tag_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    # Trouver le tag par son ID
    tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    # Suppression du tag et de ses associations
    db.delete(tag)
    db.commit()

    return {"detail": "Tag successfully deleted"}