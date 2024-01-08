import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_json_file_list(json_folder_path):
    """
    Retrieves a sorted list of all JSON file names in a specified directory.

    :param json_folder_path: Path to the directory containing JSON files.
    :return: Sorted list of JSON file names.
    """
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]
    json_files.sort()  # Sorting JSON files alphabetically by recipe ID
    return json_files


def download_image(json_folder_path, filename):
    """
    Downloads an image for a given JSON file.

    :param json_folder_path: Path to the directory containing JSON files.
    :param filename: Name of the JSON file.
    """
    file_path = os.path.join(json_folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    image_path = data.get('imagePath', None)
    if image_path:
        image_url = f"https://img.hellofresh.com/f_auto,fl_lossy,q_auto/hellofresh_s3{image_path}"
        recipe_id = os.path.splitext(filename)[0]
        recipe_folder = os.path.join(json_folder_path, recipe_id)
        os.makedirs(recipe_folder, exist_ok=True)

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(os.path.join(recipe_folder, 'cover.jpg'), 'wb') as image_file:
                image_file.write(image_response.content)
            return f"Downloaded image for recipe {recipe_id}"
        else:
            return f"Error downloading image for recipe {recipe_id}"

def parallel_image_download(json_folder_path, json_files, max_workers=10):
    """
    Downloads images in parallel from a list of JSON files.

    :param json_folder_path: Path to the directory containing JSON files.
    :param json_files: List of JSON file names.
    :param max_workers: Maximum number of threads to use.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_image, json_folder_path, filename): filename for filename in json_files}
        for future in as_completed(futures):
            filename = futures[future]
            try:
                result = future.result()
                print(f"{result} (File: {filename})")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")



# Exemple d'utilisation
files = get_json_file_list('recipes')
parallel_image_download('recipes', files, max_workers=20)
