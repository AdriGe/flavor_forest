import csv
import json
import os

# Base path
base_path = '/Users/adriengeiger/git/flavor_forest/hellofresh'

# Input and output paths
input_dir = os.path.join(base_path, 'data/recipes/json')
output_file = os.path.join(base_path, 'src/recipes.csv')

# CSV columns
columns = ['recipe_id', 'user_id', 'name', 'headline', 'description', 'total_time', 'prep_time', 'difficulty', 'utensils', 'image_url', 'favorites_count','kcal', 'fat', 'saturated_fat', 'carbohydrate', 'sugars', 'protein', 'fiber', 'sodium', 'steps']

def format_pgsql_array(array):
    """ Formats a Python list as a PostgreSQL array """
    if array is None:
        return '{}'
    return '{' + ','.join([f'"{str(item)}"' for item in array]) + '}'

def remove_small_strings(field):
    """ Return an empty string if the field is None or exactly matches a specific string """
    if field is None:
        return ''

    specific_strings = ['-', ',', '.-', '..', '.']
    if field in specific_strings:
        return ''
    return field

# Read and process each JSON file
csv_data = []
for file in os.listdir(input_dir):
    if file.endswith('.json'):
        with open(os.path.join(input_dir, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            row = {
                'recipe_id': data.get('id', ''),
                'user_id': '',  # empty column
                'name': data.get('name', ''),
                'headline': remove_small_strings(data.get('headline', '')),
                'description': remove_small_strings(data.get('description', '')),
                'total_time': data.get('totalTime', ''),
                'prep_time': data.get('prepTime', ''),
                'difficulty': data.get('difficulty', ''),
                'utensils': format_pgsql_array(data.get('utensils', [])),
                'image_url': data.get('image_id', ''),
                'favorites_count': data.get('favoritesCount', ''),
                'kcal': data.get('nutrition').get('kcal', ''),
                'fat': data.get('nutrition').get('fat', ''),
                'saturated_fat': data.get('nutrition').get('saturated_fat', ''),
                'carbohydrate': data.get('nutrition').get('carbohydrate', ''),
                'sugars': data.get('nutrition').get('sugars', ''),
                'protein': data.get('nutrition').get('protein', ''),
                'fiber': data.get('nutrition').get('fiber', ''),
                'sodium': data.get('nutrition').get('sodium', ''),
                'steps': format_pgsql_array(data.get('steps', []))
            }
            csv_data.append(row)

# Write to the CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(csv_data)
