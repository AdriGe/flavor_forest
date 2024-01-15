import json
import csv
import sys
import os
import re
import uuid

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
            key = (row['ingredient_id_old'], row['portion'])
            value = {'ingredient_id': row['ingredient_id'], 'portion_id': row['portion_id']}
            mapping[key] = value
    return mapping


def map_nutrition(name):
    mapping = {
        'Énergie (kcal)': 'kcal',
        'Glucides': 'carbohydrate',
        'dont sucres': 'sugars',
        'Matières grasses': 'fat',
        'dont acides gras saturés': 'saturated_fat',
        'Protéines': 'protein',
        'Sel': 'sodium'
    }

    return mapping.get(name, None)

def extract_numeric_part(s):
    if s is None:
        return s
    
    if s:
        return int(''.join(re.findall(r'\d+', s)))
    return s

def transform_data(input_file, output_file, mapping_file, portion_mapping_file):
    id_mapping = load_id_mapping(mapping_file)
    id_portion_mapping = load_id_portion_mapping(portion_mapping_file)

    with open(input_file, 'r') as file:
        data = json.load(file)

    # Transforming the data
    transformed_data = {}
    transformed_data['cuisines'] = [item['name'] for item in data.get('cuisines', [])]
    for field in ['description', 'difficulty', 'favoritesCount', 'headline', 'name']:
        transformed_data[field] = data.get(field)
    
    transformed_data['prepTime'] = extract_numeric_part(data.get('prepTime'))
    transformed_data['totalTime'] = extract_numeric_part(data.get('totalTime'))

    transformed_data['image_id'] = data.get('id')
    transformed_data['id'] = str(uuid.uuid4())
    transformed_data['nutrition'] = {map_nutrition(item['name']): item['amount'] for item in data.get('nutrition', []) if map_nutrition(item['name']) is not None}

    transformed_data['tags'] = [item['name'] for item in data.get('tags', [])]
    transformed_data['utensils'] = [item['name'] for item in data.get('utensils', [])]
    transformed_data['ingredients'] = []
    for item in data.get('yields', []):
        if item.get('yields') == 2 and 'ingredients' in item:
            transformed_data['ingredients'].extend(item['ingredients'])
            for ingredient in item['ingredients']:
                mapped_portion = id_portion_mapping.get((ingredient['id'], ingredient['unit']))

                if ingredient['unit'] in ['g', 'ml'] or mapped_portion is None:
                    ingredient['ingredient_id'] = id_mapping[ingredient['id']]
                else:
                    ingredient['ingredient_id'] = mapped_portion['ingredient_id']
                    ingredient['portion_id'] = mapped_portion['portion_id']
                    ingredient['image_id'] = ingredient['id']
                del ingredient['id']
   
    steps_sorted = sorted(data.get('steps', []), key=lambda x: x.get('index', 0))
    transformed_data['steps'] = [step['instructions'] for step in steps_sorted]

    # Writing the transformed data to a new file
    with open(output_file, 'w') as file:
        json.dump(transformed_data, file, ensure_ascii=False, indent=4)


def process_directory(input_dir, output_dir, mapping_file, portion_mapping_file):
    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    total_files = len(files)

    for index, filename in enumerate(files, start=1):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        print(f"Processing file {index} of {total_files}: {input_file_path}")# -> {output_file_path}")

        transform_data(input_file_path, output_file_path, mapping_file, portion_mapping_file)
        

        
        

base_path = '/Users/adriengeiger/git/flavor_forest/hellofresh'
input_dir = os.path.join(base_path, 'data/recipes/json')
output_dir = os.path.join(base_path, 'src/data/recipes_out')
mapping_file = os.path.join(base_path, 'data/ingredients/match_ids.csv')
portion_mapping_file = os.path.join(base_path, 'data/portions/match_portions_ids.csv')

process_directory(input_dir, output_dir, mapping_file, portion_mapping_file)
