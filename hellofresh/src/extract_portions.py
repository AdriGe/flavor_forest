import json
import csv
import os

# Mettez le chemin vers le dossier contenant vos fichiers JSON ici
json_folder_path = '/Users/adriengeiger/git/flavor_forest/hellofresh/data/recipes/json'

# Name of the output CSV file
csv_file_name = 'recipes.csv'

# Create and open the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header of the CSV file
    csv_writer.writerow(['recipe_id', 'ingredient_id', 'unit', 'amount'])

    # Iterate over all JSON files in the folder
    for file_name in os.listdir(json_folder_path):
        if file_name.endswith('.json'):
            full_path = os.path.join(json_folder_path, file_name)

            # Read the JSON file
            with open(full_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                recipe_id = data['id']  # Make sure the field is named 'id'

                # Extract data for each ingredient
                for yield_item in data['yields']:
                    if yield_item['yields'] == 2:
                        for item in yield_item['ingredients']:
                            ingredient_id = item['id']
                            unit = item['unit']
                            amount = item['amount']
                            # Write the data to the CSV file
                            csv_writer.writerow([recipe_id, ingredient_id, unit, amount])
