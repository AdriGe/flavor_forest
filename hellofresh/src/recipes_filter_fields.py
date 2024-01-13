import json
import csv
import sys

def load_id_mapping(csv_file):
    mapping = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mapping[row['id_old']] = row['id']
    return mapping


def load_id_portion_mapping(csv_file):
    mapping = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['ingredient_id_old'], row['name'])
            value = {'new_id': row['ingredient_id'], 'portion': row['name']}
            mapping[key] = value
    return mapping

def transform_data(input_file, output_file, mapping_file, portion_mapping_file):
    id_mapping = load_id_mapping(mapping_file)
    id_portion_mapping = load_id_portion_mapping(portion_mapping_file)


    with open(input_file, 'r') as file:
        data = json.load(file)

    # Transforming the data
    transformed_data = {}
    transformed_data['cuisines'] = [item['name'] for item in data.get('cuisines', [])]
    for field in ['description', 'difficulty', 'favoritesCount', 'headline', 'name', 'prepTime', 'totalTime']:
        transformed_data[field] = data.get(field)
    transformed_data['recipe_id_old'] = data.get('id')
    transformed_data['nutrition'] = [{key: value for key, value in item.items() if key in ['name', 'amount', 'unit']} for item in data.get('nutrition', [])]
    transformed_data['tags'] = [item['name'] for item in data.get('tags', [])]
    transformed_data['utensils'] = [item['name'] for item in data.get('utensils', [])]
    transformed_data['yields'] = []
    for item in data.get('yields', []):
        if item.get('unit') not in ['g', 'ml']:
            key = (item.get('id'), item.get('unit'))
            if key in id_portion_mapping:
                new_item = id_portion_mapping[key]
                transformed_data['yields'].append(new_item)
            else:
                sys.exit(f"Error: No matching new_id and portion found for id '{item.get('id')}' and unit '{item.get('unit')}'")

    transformed_data['ingredients'] = []
    for item in data.get('ingredients', []):
        if 'id' in item and 'name' in item:
            old_id = item['id']
            if old_id not in id_mapping:
                sys.exit(f"Error: No new ID found for old ID '{old_id}'")
            new_item = {'id': id_mapping[old_id], 'name': item['name']}
            transformed_data['ingredients'].append(new_item)
   
    transformed_data['steps'] = [{key: item[key] for key in ['index', 'instructions']} for item in data.get('steps', []) if 'index' in item and 'instructions' in item]

    # Writing the transformed data to a new file
    with open(output_file, 'w') as file:
        json.dump(transformed_data, file, ensure_ascii=False, indent=4)


base_path = '/Users/adriengeiger/git/flavor_forest/hellofresh'
input_dir = f'{base_path}/src/data/recipes_in/5afbf80b30006c5464684052.json'
output_dir = f'{base_path}/src/data/recipes_out/5afbf80b30006c5464684052.json'
mapping_file = f'{base_path}/data/ingredients/match_ids.csv'
portion_mapping_file = f'{base_path}/data/portions/match_portions_ids.csv'
# Example usage
transform_data(input_dir, output_dir, mapping_file, portion_mapping_file)