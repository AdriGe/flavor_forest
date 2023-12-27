from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db, SessionLocal
from models.recipes import Recipe, RecipeFood, Step, Tag, RecipeTag
from schemas.recipes import RecipeCreate, RecipeDetail, RecipeFoodDetail, TagDetail, StepDetail, RecipeUpdate, RecipeTagsUpdate, FoodDetail
from sqlalchemy import text
import json

def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

router = APIRouter()

@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):

    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    return db_recipe


@router.post("", response_model=RecipeDetail)
def create_recipe(recipe: RecipeCreate, db: SessionLocal = Depends(get_db)):
    # Création de la nouvelle recette
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        total_time=recipe.total_time,
        prep_time=recipe.prep_time,
        difficulty=recipe.difficulty,
        ustensils=recipe.ustensils,
        image_url=recipe.image_url,
        user_id=recipe.user_id,
        steps=[Step(**step.dict()) for step in recipe.steps],
        tags=[db.query(Tag).filter(Tag.tag_id == tag_id).first() for tag_id in recipe.tags],
        foods=[RecipeFood(food_id=food.food_id, quantity=food.quantity, portion_id=food.portion_id) for food in recipe.foods]
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Traitement des détails de chaque ingrédient de la recette
    enriched_foods = []
    for food in new_recipe.foods:
        enriched_food = RecipeFoodDetail(
            food_id=food.food_id,
            food_name=food.food.name,
            quantity=food.quantity,
            measurement=food.portion.name if food.portion else food.food.unit.name
        )
        enriched_foods.append(enriched_food)

    # Construction de l'objet RecipeDetail pour la réponse
    recipe_detail = RecipeDetail(
        recipe_id=new_recipe.recipe_id,
        user_id=new_recipe.user_id,
        title=new_recipe.title,
        description=new_recipe.description,
        total_time=new_recipe.total_time,
        prep_time=new_recipe.prep_time,
        difficulty=new_recipe.difficulty,
        ustensils=new_recipe.ustensils,
        image_url=new_recipe.image_url,
        steps=[StepDetail(**model_to_dict(step)) for step in new_recipe.steps],
        foods=enriched_foods,
        tags=[TagDetail(tag_id=tag.tag_id, name=tag.name) for tag in new_recipe.tags]
    )

    return recipe_detail


@router.put("/{recipe_id}", response_model=RecipeDetail)
def update_recipe(recipe_id: int, recipe_data: RecipeUpdate, db: SessionLocal = Depends(get_db)):
    # Trouver la recette par ID
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Mise à jour des champs de la recette
    for key, value in recipe_data.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)

    db.commit()
    db.refresh(db_recipe)

    # Traitement des détails de chaque ingrédient de la recette
    enriched_foods = []
    for food in db_recipe.foods:
        enriched_food = RecipeFoodDetail(
            food_id=food.food_id,
            food_name=food.food.name,
            quantity=food.quantity,
            measurement=food.portion.name if food.portion else food.food.unit.name
        )
        enriched_foods.append(enriched_food)

    recipe_detail = RecipeDetail(
        recipe_id=db_recipe.recipe_id,
        user_id=db_recipe.user_id,
        title=db_recipe.title,
        description=db_recipe.description,
        total_time=db_recipe.total_time,
        prep_time=db_recipe.prep_time,
        difficulty=db_recipe.difficulty,
        ustensils=db_recipe.ustensils,
        image_url=db_recipe.image_url,
        steps=[StepDetail(**model_to_dict(step)) for step in db_recipe.steps],
        foods=enriched_foods,
        tags=[TagDetail(tag_id=tag.tag_id, name=tag.name) for tag in db_recipe.tags]
    )

    # Retourner la recette mise à jour
    return recipe_detail


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete(synchronize_session=False)
    db.query(RecipeFood).filter(RecipeFood.recipe_id == recipe_id).delete(synchronize_session=False)
    db.query(Step).filter(Step.recipe_id == recipe_id).delete(synchronize_session=False)
    
    # Supprimer la recette
    db_recipe = db.query(Recipe).get(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()

    return {"detail": "Recipe successfully deleted"}

#### TODO Fix case when tag_id does not exist
@router.put("/{recipe_id}/tags")
def update_recipe_tags(recipe_id: int, tags_data: RecipeTagsUpdate, db: SessionLocal = Depends(get_db)):
    # Trouver la recette
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Mise à jour des tags associés à la recette
    # Supprimer tous les enregistrements existants de recipe_tags pour cette recette
    db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete(synchronize_session="fetch")

    # Ajouter les nouveaux enregistrements de tags
    new_tags = [RecipeTag(recipe_id=recipe_id, tag_id=tag_id) for tag_id in tags_data.tags]
    db.add_all(new_tags)

    db.commit()

    return {"detail": "Recipe tags updated successfully"}
