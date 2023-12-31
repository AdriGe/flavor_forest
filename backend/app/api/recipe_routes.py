from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import get_db, SessionLocal, model_to_dict
from models.recipes import Recipe, RecipeFood, RecipeTag
from models.tags import Tag
from models.steps import Step
from schemas.recipes import RecipeCreate, RecipeDetail, RecipeFoodDetail, TagDetail, StepDetail, RecipeUpdate, RecipeTagsUpdate, RecipeStepsUpdate, RecipeListResponse
from sqlalchemy import func
import unidecode
from typing import List, Optional


def cast_recipe_to_recipe_detail(recipe: Recipe) -> RecipeDetail:
    # Traitement des détails de chaque ingrédient de la recette
    enriched_foods = []
    for food in recipe.foods:
        enriched_food = RecipeFoodDetail(
            food_id=food.food_id,
            food_name=food.food.name,
            quantity=food.quantity,
            measurement=food.portion.name if food.portion else food.food.unit.name
        )
        enriched_foods.append(enriched_food)

    # Construction de l'objet RecipeDetail pour la réponse
    recipe_detail = RecipeDetail(
        recipe_id=recipe.recipe_id,
        user_id=recipe.user_id,
        title=recipe.title,
        description=recipe.description,
        total_time=recipe.total_time,
        prep_time=recipe.prep_time,
        difficulty=recipe.difficulty,
        ustensils=recipe.ustensils,
        image_url=recipe.image_url,
        steps=[StepDetail(**model_to_dict(step)) for step in recipe.steps],
        foods=enriched_foods,
        tags=[TagDetail(tag_id=tag.tag_id, name=tag.name) for tag in recipe.tags]
    )

    return recipe_detail

router = APIRouter()

@router.get("", response_model=RecipeListResponse)
def get_recipes(
    tags: Optional[List[str]] = Query(None),
    difficulty: Optional[str] = None,
    preparation_time: Optional[int] = None,
    title: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: SessionLocal = Depends(get_db)
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid page or page_size parameters")

    query = db.query(Recipe)

    if tags:
        for tag in tags:
            query = query.filter(Recipe.tags.any(Tag.name == tag))
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)
    if preparation_time:
        query = query.filter(Recipe.preparation_time <= preparation_time)
    if title:
        search_words = title.split()
        for word in search_words:
            normalized_word = unidecode.unidecode(word)  # Normalisation des accents
            query = query.filter(func.lower(Recipe.title).like(f"%{normalized_word.lower()}%"))


    recipes = query.all()

    

    total_recipes = query.count()  # Nombre total de recettes répondant aux filtres
    total_pages = (total_recipes + page_size - 1) // page_size  # Calcul du nombre total de pages

    skip = (page - 1) * page_size
    recipes = query.offset(skip).limit(page_size).all()
    recipes_casted = [cast_recipe_to_recipe_detail(new_recipe) for new_recipe in recipes]

    return RecipeListResponse(
        total_recipes=total_recipes,
        total_pages=total_pages,
        recipes=recipes_casted
    )


@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):

    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    recipe_detail = cast_recipe_to_recipe_detail(db_recipe)

    return recipe_detail


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

    recipe_detail = cast_recipe_to_recipe_detail(new_recipe)

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

    recipe_detail = cast_recipe_to_recipe_detail(db_recipe)

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


@router.put("/{recipe_id}/tags")
def update_recipe_tags(recipe_id: int, tags_data: RecipeTagsUpdate, db: SessionLocal = Depends(get_db)):
    # Trouver la recette
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Vérifier l'existence de chaque tag
    for tag_id in tags_data.tags:
        existing_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
        if not existing_tag:
            raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    # Mise à jour des tags associés à la recette
    # Supprimer tous les enregistrements existants de recipe_tags pour cette recette
    db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete(synchronize_session="fetch")

    # Ajouter les nouveaux enregistrements de tags
    new_tags = [RecipeTag(recipe_id=recipe_id, tag_id=tag_id) for tag_id in tags_data.tags]
    db.add_all(new_tags)

    db.commit()

    return {"detail": "Recipe tags updated successfully"}


@router.put("/{recipe_id}/steps")
def update_recipe_steps(recipe_id: int, steps_data: RecipeStepsUpdate, db: SessionLocal = Depends(get_db)):
    # Trouver la recette par son ID
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Supprimer les anciennes étapes
    db.query(Step).filter(Step.recipe_id == recipe_id).delete()

    # Ajouter les nouvelles étapes
    new_steps = [Step(recipe_id=recipe_id, **step.dict()) for step in steps_data.steps]
    db.add_all(new_steps)

    db.commit()

    return {"detail": "Recipe steps updated successfully"}
