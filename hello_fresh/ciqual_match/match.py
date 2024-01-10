import os
import pandas as pd
from Levenshtein import ratio


def load_data(hellofresh_csv_path, ciqual_csv_path):
    try:
        hellofresh_data = pd.read_csv(hellofresh_csv_path, usecols=['id', 'name', 'category'])
        ciqual_data = pd.read_csv(ciqual_csv_path)
        return hellofresh_data, ciqual_data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None, None, str(e)


def find_probable_matches(ingredient, ciqual_data):
    print(ingredient)
    ciqual_data['similarity'] = ciqual_data['alim_nom_fr'].apply(lambda x: ratio(ingredient.lower(), x.lower()))
    probable_matches = ciqual_data.sort_values(by='similarity', ascending=False).head(20)
    return probable_matches


def interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename):
    hellofresh_data, ciqual_data = load_data(hellofresh_csv_path, ciqual_csv_path)
    if hellofresh_data is None or ciqual_data is None:
        return "Failed to load data."

    matches = []

    for index, row in hellofresh_data.iterrows():
        probable_matches = find_probable_matches(row['name'], ciqual_data)
        
        while True:
            print(f"\nProcessing ingredient {index+1}/{len(hellofresh_data)}: {row['name']}")
            print("0: Pas de correspondance")
            for idx, match in enumerate(probable_matches.itertuples(), 1):
                print(f"{idx}: {match.alim_nom_fr} (Similarity: {match.similarity:.2f})")
            
            chosen_match_index = input("Enter the number of the chosen match (enter '0' if none): ")
            if not chosen_match_index.isdigit() or not 0 <= int(chosen_match_index) <= 20:
                print("Invalid selection. Please enter a number between 0 and 20.")
                continue
            
            chosen_match_index = int(chosen_match_index) - 1
            if chosen_match_index == -1:
                chosen_match_name = "Pas de correspondance"
                chosen_ciqual_id = None
            else:
                chosen_match = probable_matches.iloc[chosen_match_index]
                chosen_match_name = chosen_match['alim_nom_fr']
                chosen_ciqual_id = chosen_match['id']

            matches.append({
                'hellofresh_id': row['id'],
                'ciqual_id': chosen_ciqual_id,
                'ciqual_alim_nom_fr': chosen_match_name
            })
            break

    matches_df = pd.DataFrame(matches)
    matches_df.to_csv(output_filename, index=False)
    print(f"\nMatching complete. Results saved to '{output_filename}'.")
    return matches_df
    

base_path = '/Users/adriengeiger/git/flavor_forest/hello_fresh/ciqual_match/hellofresh_generic'
hellofresh_csv_path = f"{base_path}/generic_hellofresh_10.csv" # This is an example path
output_filename = f"match_{os.path.basename(hellofresh_csv_path)}" # This is an example path
ciqual_csv_path = f"{base_path}/../ciqual.csv" # This is an example path

matches_df = interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename)
