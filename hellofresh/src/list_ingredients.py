import os
import json

def list_json_files(json_folder_path):
    """
    List all JSON files in the specified folder.
    :param json_folder_path: Path to the directory containing JSON files.
    :return: List of paths to JSON files.
    """
    json_files = [os.path.join(json_folder_path, f) for f in os.listdir(json_folder_path) if f.endswith('.json')]
    json_files.sort()  # Sorting JSON files alphabetically by recipe ID
    return json_files

def extract_unique_ingredient_names(json_files):
    """
    Extract and deduplicate ingredient names from JSON files.
    :param json_files: List of paths to JSON files.
    :return: Set of unique ingredient names.
    """
    ingredient_names = set()

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            recipe_data = json.load(file)
            for ingredient in recipe_data.get("ingredients", []):
                ingredient_name = ingredient.get("name")
                ingredient_id = ingredient.get("id")
                try:
                    ingredient_family = ingredient.get("family").get("name")
                except:
                    ingredient_family = ""

                if ingredient_family.lower() == "none":
                    ingredient_family = ""

                ingredient_names.add(f"\"{ingredient_id}\",\"{ingredient_name}\",\"{ingredient_family}\"")
                

    return ingredient_names

# Replace '/path/to/json/folder' with the actual path where your JSON files are stored
json_folder_path = '/home/adrien/git/flavor_forest/hello_fresh/data/recipes'
json_files = list_json_files(json_folder_path)
unique_ingredient_names = extract_unique_ingredient_names(json_files)

# Example action with extracted ingredient names
for name in unique_ingredient_names:
    print(f"{name}")
