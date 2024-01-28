from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import get_db, SessionLocal, model_to_dict
from models.recipes import Recipe, RecipeFood, RecipeTag
from models.tags import Tag
from schemas.recipes import RecipeCreate, RecipeDetail, RecipeFoodDetail, TagDetail, RecipeUpdate, RecipeTagsUpdate, RecipeListResponse
from models.user import User
from models.foods import Food
from models.portions import Portion
from sqlalchemy import func
import unidecode
from typing import List, Optional
from datetime import datetime
import uuid
from api.user_routes import get_current_user

def cast_recipe_to_recipe_detail(recipe: Recipe) -> RecipeDetail:
    # Traitement des détails de chaque ingrédient de la recette
    enriched_foods = []
    for food in recipe.foods:
        enriched_food = RecipeFoodDetail(
            food_id=food.food_id,
            food_name=food.food.name,
            quantity=food.quantity,
            portion_id=food.portion_id,
            unit=food.portion.name if food.portion else food.food.unit.name,
            image_url=food.food.image_url
        )
        enriched_foods.append(enriched_food)

    # Construction de l'objet RecipeDetail pour la réponse
    recipe_detail = RecipeDetail(
        recipe_id=recipe.recipe_id,
        user_id=recipe.user_id,
        name=recipe.name,
        headline=recipe.headline,
        description=recipe.description,
        total_time=recipe.total_time,
        prep_time=recipe.prep_time,
        difficulty=recipe.difficulty,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at,
        utensils=recipe.utensils,
        image_url=recipe.image_url,
        favorites_count=recipe.favorites_count,
        kcal=recipe.kcal,
        fat=recipe.fat,
        saturated_fat=recipe.saturated_fat,
        carbohydrate=recipe.carbohydrate,
        sugars=recipe.sugars,
        protein=recipe.protein,
        fiber=recipe.fiber,
        sodium=recipe.sodium,
        serving_size=recipe.serving_size,
        steps=recipe.steps,
        steps_images_url=recipe.steps_images_url,
        foods=enriched_foods,
        tags=[TagDetail(tag_id=tag.tag_id, name=tag.name, category=tag.category) for tag in recipe.tags]
    )

    return recipe_detail

router = APIRouter()

@router.get("", response_model=RecipeListResponse)
def get_recipes(
    tags: Optional[List[str]] = Query(None),
    difficulty: Optional[str] = None,
    preparation_time: Optional[int] = None,
    total_time: Optional[int] = None,
    name: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    if total_time:
        query = query.filter(Recipe.total_time <= total_time)
    if name:
        search_words = name.split()
        for word in search_words:
            normalized_word = unidecode.unidecode(word)  # Normalisation des accents
            query = query.filter(func.lower(Recipe.name).like(f"%{normalized_word.lower()}%"))

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
def get_recipe(
    recipe_id: uuid.UUID, 
    db: SessionLocal = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):

    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    recipe_detail = cast_recipe_to_recipe_detail(db_recipe)

    return recipe_detail


@router.post("", response_model=RecipeDetail)
def create_recipe(recipe: RecipeCreate, db: SessionLocal = Depends(get_db)):
    # Création de la nouvelle recette
    new_recipe = Recipe(
        user_id=None,
        name=recipe.name,
        headline=recipe.headline,
        description=recipe.description,
        total_time=recipe.total_time,
        prep_time=recipe.prep_time,
        difficulty=recipe.difficulty,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        utensils=recipe.utensils,
        image_url=recipe.image_url,
        favorites_count=0,
        kcal=recipe.kcal,
        fat=recipe.fat,
        saturated_fat=recipe.saturated_fat,
        carbohydrate=recipe.carbohydrate,
        sugars=recipe.sugars,
        protein=recipe.protein,
        fiber=recipe.fiber,
        sodium=recipe.sodium,
        steps=recipe.steps,
        steps_images_url=recipe.steps_images_url,
        tags=[db.query(Tag).filter(Tag.tag_id == tag_id).first() for tag_id in recipe.tags],
        foods=[RecipeFood(food_id=food.food_id, quantity=food.quantity, portion_id=food.portion_id) for food in recipe.foods]
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    recipe_detail = cast_recipe_to_recipe_detail(new_recipe)

    return recipe_detail


@router.put("/{recipe_id}", response_model=RecipeDetail)
def update_recipe(
    recipe_id: uuid.UUID, 
    recipe_data: RecipeUpdate, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Trouver la recette par ID
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Mise à jour des champs de la recette
    for key, value in recipe_data.dict(exclude_unset=True, exclude={"tags", "foods"}).items():
        setattr(db_recipe, key, value)

    # Mise à jour des tags
    if recipe_data.tags is not None:
        for tag_id in recipe_data.tags:
            existing_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
            if not existing_tag:
                raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")
       
        # Supprimez tous les tags existants pour cette recette
        db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete()
        # Ajoutez les nouveaux tags
        for tag_id in recipe_data.tags:
            new_recipe_tag = RecipeTag(recipe_id=recipe_id, tag_id=tag_id)
            db.add(new_recipe_tag)

    # Mise à jour des foods et portions
    if recipe_data.foods is not None:
        for food_data in recipe_data.foods:
        # Vérifiez si le food_id existe
            existing_food = db.query(Food).filter(Food.food_id == food_data.food_id).first()
            if not existing_food:
                raise HTTPException(status_code=404, detail=f"Food with ID {food_data.food_id} not found")

            # Vérifiez si le portion_id existe (si fourni)
            if food_data.portion_id:
                existing_portion = db.query(Portion).filter(Portion.portion_id == food_data.portion_id).first()
                if not existing_portion:
                    raise HTTPException(status_code=404, detail=f"Portion with ID {food_data.portion_id} not found")

        # Supprimez toutes les associations de foods existantes pour cette recette
        db.query(RecipeFood).filter(RecipeFood.recipe_id == recipe_id).delete()

        # Ajoutez les nouvelles associations de foods
        for food_data in recipe_data.foods:
            new_recipe_food = RecipeFood(
                recipe_id=recipe_id,
                food_id=food_data.food_id,
                quantity=food_data.quantity,
                portion_id=getattr(food_data, 'portion_id', None)
            )
            db.add(new_recipe_food)

    db.commit()
    db.refresh(db_recipe)

    recipe_detail = cast_recipe_to_recipe_detail(db_recipe)
    return recipe_detail


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: uuid.UUID, 
    db: SessionLocal = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete(synchronize_session=False)
    db.query(RecipeFood).filter(RecipeFood.recipe_id == recipe_id).delete(synchronize_session=False)

    # Supprimer la recette
    db_recipe = db.query(Recipe).get(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()

    return {"detail": "Recipe successfully deleted"}

