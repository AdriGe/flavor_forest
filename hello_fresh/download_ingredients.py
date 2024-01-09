import os
import json
import requests
import concurrent.futures

def list_json_files(json_folder_path):
    """
    List all JSON files in the specified folder.

    :param json_folder_path: Path to the directory containing JSON files.
    :return: List of paths to JSON files.
    """
    json_files = [os.path.join(json_folder_path, f) for f in os.listdir(json_folder_path) if f.endswith('.json')]
    json_files.sort()  # Sorting JSON files alphabetically by recipe ID
    return json_files


def extract_ingredients(json_files):
    """
    Extract and deduplicate ingredients from JSON files.

    :param json_files: List of paths to JSON files.
    :return: Set of tuples with (ingredient_id, image_path).
    """
    ingredients = set()

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            recipe_data = json.load(file)
            for ingredient in recipe_data.get("ingredients", []):
                ingredient_id = ingredient.get("id")
                image_path = ingredient.get("imagePath")
                if ingredient_id and image_path:
                    ingredients.add((ingredient_id, image_path))

    return ingredients


def download_ingredient_image(ingredient, base_url="https://img.hellofresh.com/c_fill,f_auto,fl_lossy,h_300,q_auto,w_300/hellofresh_s3"):
    """
    Download an image for a single ingredient.

    :param ingredient: Tuple with (ingredient_id, image_path).
    :param base_url: Base URL for image download.
    """
    ingredient_id, image_path = ingredient
    image_url = f"{base_url}/{image_path}"
    response = requests.get(image_url)
    if response.status_code == 200:
        os.makedirs('ingredients', exist_ok=True)
        with open(os.path.join('ingredients', f'{ingredient_id}.jpg'), 'wb') as file:
            file.write(response.content)
            print(f"Image for ingredient {ingredient_id} downloaded successfully.")
    else:
        print(f"Error downloading image for ingredient {ingredient_id}: {response.status_code}")


def download_ingredient_images_concurrently(unique_ingredients, max_workers=20):
    """
    Download images for all unique ingredients concurrently.

    :param unique_ingredients: Set of tuples with (ingredient_id, image_path).
    :param max_workers: Maximum number of threads to use for concurrent downloads.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(download_ingredient_image, unique_ingredients)

# Exemple d'utilisation
json_files = list_json_files("recipes")
unique_ingredients = extract_ingredients(json_files)
download_ingredient_images_concurrently(unique_ingredients, max_workers=20)
