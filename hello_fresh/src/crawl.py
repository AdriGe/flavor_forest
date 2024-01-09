import requests
import os
import json
import sys
import time
import random
from datetime import datetime, timedelta
import brotli

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def random_sleep(min_milliseconds, max_milliseconds):
    sleep_time = random.uniform(min_milliseconds / 1000, max_milliseconds / 1000)
    print(f"Sleeping for {sleep_time}ms ...")
    time.sleep(sleep_time)


def generate_weeks_list(start_year_week, end_year_week):
    start_year, start_week = map(int, start_year_week.split('-W'))
    end_year, end_week = map(int, end_year_week.split('-W'))

    start_date = datetime.strptime(f'{start_year} {start_week} 1', '%G %V %u')
    end_date = datetime.strptime(f'{end_year} {end_week} 1', '%G %V %u')

    current_date = start_date
    weeks = []

    while current_date <= end_date:
        year_week = current_date.strftime('%G-W%V')
        weeks.append(year_week)
        current_date += timedelta(weeks=1)

    return weeks

def fetch_hellofresh_data(weeks, auth_token):
    base_url = "https://www.hellofresh.fr/gw/my-deliveries/menu"
    params = {
        "locale": "fr-FR",
        "postcode": "75019",
        "servings": 2,
        "subscription": 1304935,
        "product-sku": "FR-CBT3-3-2-0"
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    recipe_ids = []
    os.makedirs('weeks', exist_ok=True)

    for week in weeks:
        params["week"] = week
        response = requests.get(base_url, headers=headers, params=params)
        
        print(f"Traitement de la semaine : {week}")
        print(f"URL demandée : {response.url}")

        if response.status_code != 200:
            try:
                # Tentative de récupérer le message d'erreur depuis le JSON
                error_message = response.json().get('errors', [{}])[0].get('message', 'Aucun message d\'erreur spécifique')
            except json.JSONDecodeError:
                # Si la réponse n'est pas un JSON, utiliser le texte de la réponse
                error_message = response.text

            print(f"Erreur : {response.status_code} - {error_message}")
            sys.exit(1)

        data = response.json()
        recipe_ids.extend([meal['recipe']['id'] for meal in data.get("meals", [])])

        with open(f'weeks/{week}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return recipe_ids



def fetch_and_save_recipe_details(recipe_ids, auth_token):
    #random_sleep(100, 2000)
    unique_recipe_ids = list(set(recipe_ids))

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {auth_token}",
        "x-requested-by": "web-foundation",
        "Alt-Used": "www.hellofresh.fr",
        "Connection": "keep-alive",
        "Referer": "https://www.hellofresh.fr/my-account/deliveries/menu?locale=fr-FR&subscriptionId=1304935&week=2024-W02&recipePreviewId=64fb2dce786cce2df0e019b8"
    }

    total_recipes = len(unique_recipe_ids)

    for index, recipe_id in enumerate(unique_recipe_ids, start=1):
        url = f"https://www.hellofresh.fr/gw/recipes/recipes/{recipe_id}"
        print(f"Recipe {index}/{total_recipes}: {url}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching recipe {recipe_id}: {response.status_code}")
            continue
        
        recipe_details = response.json()
        with open(f'recipes/{recipe_id}.json', 'w', encoding='utf-8') as file:
            json.dump(recipe_details, file, ensure_ascii=False, indent=4)


weeks = generate_weeks_list("2018-W20", "2018-W52")
config_file = 'config.json'  # Nom de votre fichier de configuration
config = load_config(config_file)
auth_token = config.get('auth_token')

recipe_ids = fetch_hellofresh_data(weeks, auth_token)

fetch_and_save_recipe_details(recipe_ids, auth_token)

print(recipe_ids)
