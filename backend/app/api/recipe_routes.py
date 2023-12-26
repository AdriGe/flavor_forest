from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db, SessionLocal
from models.recipes import Recipe, RecipeFood, Step, Tag, RecipeTag
from schemas.recipes import RecipeCreate, RecipeDetail, RecipeFoodDetail, TagDetail, StepDetail, RecipeUpdate

def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

router = APIRouter()

@router.post("", response_model=RecipeDetail)
def create_recipe(recipe: RecipeCreate, db: SessionLocal = Depends(get_db)):
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
        foods=[RecipeFood(**food.dict()) for food in recipe.foods]
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

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
        foods=[RecipeFoodDetail(**model_to_dict(food)) for food in new_recipe.foods],
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

    # Retourner la recette mise à jour
    return db_recipe


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
