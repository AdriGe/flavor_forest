from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.recipes import Recipe, RecipeFood, Step, Tag
from schemas.recipes import RecipeCreate, RecipeDetail, RecipeFoodDetail, TagDetail, StepDetail

def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

router = APIRouter()

@router.post("", response_model=RecipeDetail)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
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
