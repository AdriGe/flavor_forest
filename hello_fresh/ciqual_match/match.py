import os
import pandas as pd
from Levenshtein import ratio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(hellofresh_csv_path, ciqual_csv_path):
    try:
        hellofresh_data = pd.read_csv(hellofresh_csv_path, usecols=['id', 'name', 'category'])
        ciqual_data = pd.read_csv(ciqual_csv_path)
        return hellofresh_data, ciqual_data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None, None, str(e)


def find_probable_matches_levenshtein(ingredient, ciqual_data):
    ciqual_data['similarity'] = ciqual_data['alim_nom_fr'].apply(lambda x: ratio(ingredient.lower(), x.lower()))
    probable_matches = ciqual_data.sort_values(by='similarity', ascending=False).head(20)
    return probable_matches


def find_probable_matches_tfidf(ingredient, ciqual_data, vectorizer, tfidf_matrix):
    # Vectorize the current HelloFresh ingredient using the fitted vectorizer
    ingredient_vector = vectorizer.transform([ingredient])
    # Compute cosine similarity scores
    cosine_scores = cosine_similarity(ingredient_vector, tfidf_matrix)
    # Get the top 20 matches and their indices
    top_indices = cosine_scores.argsort()[0][-20:][::-1]
    # Extract the matching rows and their similarity scores
    matches = ciqual_data.iloc[top_indices].copy()  # Faire une copie explicite ici
    matches['similarity'] = cosine_scores[0, top_indices]
    return matches[['alim_code', 'alim_nom_fr', 'similarity', 'id']].reset_index(drop=True)


def display_matches(matches):
    for i, match in enumerate(matches.itertuples(), 1):
        print(f"{i}: {match.alim_nom_fr} (Score: {match.similarity:.2f})")


def interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename):
    hellofresh_data, ciqual_data = load_data(hellofresh_csv_path, ciqual_csv_path)
    if hellofresh_data is None or ciqual_data is None:
        return "Failed to load data."

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(ciqual_data['alim_nom_fr'].dropna().astype(str))

    matches = []

    for index, row in hellofresh_data.iterrows():
        print(f"\nProcessing ingredient {index+1}/{len(hellofresh_data)}: {row['name']}")

        tfidf_matches = find_probable_matches_tfidf(row['name'], ciqual_data, vectorizer, tfidf_matrix)
        display_matches(tfidf_matches)

        chosen_match_index = input("Enter the number of the chosen match (enter '0' if none): ")
        while not chosen_match_index.isdigit() or int(chosen_match_index) < 0 or int(chosen_match_index) > len(tfidf_matches):
            print("Invalid input. Please enter a valid number.")
            chosen_match_index = input("Enter the number of the chosen match (enter '0' if none): ")

        chosen_match_index = int(chosen_match_index)
        if chosen_match_index == 0:
            print("No suitable TF-IDF match. Trying Levenshtein method...")
            levenshtein_matches = find_probable_matches_levenshtein(row['name'], ciqual_data)
            display_matches(levenshtein_matches)

            chosen_match_index = input("Enter the number of the chosen Levenshtein match (enter '0' if none): ")
            while not chosen_match_index.isdigit() or int(chosen_match_index) < 0 or int(chosen_match_index) > len(levenshtein_matches):
                print("Invalid input. Please enter a valid number.")
                chosen_match_index = input("Enter the number of the chosen Levenshtein match (enter '0' if none): ")

            chosen_match_index = int(chosen_match_index)
            if chosen_match_index == 0:
                chosen_match_name = "Pas de correspondance"
                chosen_match_id = ''
            else:
                chosen_match = levenshtein_matches.iloc[chosen_match_index - 1]
                chosen_match_name = chosen_match['alim_nom_fr']
                chosen_match_id = chosen_match['id']
        else:
            chosen_match = tfidf_matches.iloc[chosen_match_index - 1]
            chosen_match_name = chosen_match['alim_nom_fr']
            chosen_match_id = chosen_match['id']

        matches.append({
            'hellofresh_id': row['id'],
            'ciqual_id': chosen_match_id,
            'ciqual_alim_nom_fr': chosen_match_name
        })

    matches_df = pd.DataFrame(matches)
    matches_df.to_csv(output_filename, index=False)
    print("\nMatching complete. Results saved to", output_filename)
    return matches_df
    

base_path = '~/git/flavor_forest/hello_fresh/ciqual_match/hellofresh_generic'
hellofresh_csv_path = f"{base_path}/generic_hellofresh_99.csv" # This is an example path
output_filename = f"match_{os.path.basename(hellofresh_csv_path)}" # This is an example path
ciqual_csv_path = f"{base_path}/../ciqual.csv" # This is an example path
fasttext_model_path = f"{base_path}/../../dependencies/fasttext_models/cc.fr.300.bin" # This is an example path

matches_df = interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename)
