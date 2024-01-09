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


def download_image_step(json_file, step, base_url="https://img.hellofresh.com/f_auto,fl_lossy,q_auto/hellofresh_s3"):
    """
    Download a single image step for a recipe.

    :param json_file: Path to the JSON file.
    :param step: Step dictionary containing image info.
    :param base_url: Base URL for the image.
    """
    recipe_id = os.path.splitext(os.path.basename(json_file))[0]
    step_number = step['index']
    if step['images']:
        image_path = step['images'][0]['path']
        image_url = f"{base_url}/{image_path}"

        # Create directory if it doesn't exist
        recipe_dir = os.path.join(os.path.dirname(json_file), recipe_id)
        os.makedirs(recipe_dir, exist_ok=True)

        # Download and save the image
        print(f"Downloading image for step {step_number} of recipe {recipe_id}...")
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(os.path.join(recipe_dir, f"{step_number}.jpg"), 'wb') as img_file:
                img_file.write(image_response.content)
            print(f"Image for step {step_number} of recipe {recipe_id} downloaded successfully.")
        else:
            print(f"Error downloading image for step {step_number} of recipe {recipe_id}: {image_response.status_code}")

def download_step_images(json_files, max_workers=30):
    """
    Download step images from each recipe JSON file using parallel execution.

    :param json_files: List of paths to JSON files.
    :param max_workers: Maximum number of threads to use.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as file:
                recipe_data = json.load(file)

            steps = recipe_data.get('steps', [])

            for step in steps:
                futures.append(executor.submit(download_image_step, json_file, step))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        print(f"Completed downloading images for all recipes.")




json_folder_path = 'recipes'
json_files = list_json_files(json_folder_path)
download_step_images(json_files)