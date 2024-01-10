import os
import pandas as pd
from Levenshtein import ratio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image, ImageTk
import tkinter as tk
import os
import threading

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
        print(f"{i:02d}: {match.alim_nom_fr} (Score: {match.similarity:.2f})")


def display_image(image_path):
    def open_image():
        if os.path.exists(image_path):
            root = tk.Tk()
            img = Image.open(image_path)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(root, image=img)
            panel.pack(side="bottom", fill="both", expand="yes")

            # Fermer automatiquement après 1 seconde
            root.after(1000, lambda: root.destroy())

            root.mainloop()
        else:
            print("Image not found.")

    thread = threading.Thread(target=open_image)
    thread.start()

    

def interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename, images_directory):
    hellofresh_data, ciqual_data = load_data(hellofresh_csv_path, ciqual_csv_path)
    if hellofresh_data is None or ciqual_data is None:
        return "Failed to load data."

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(ciqual_data['alim_nom_fr'].dropna().astype(str))

    matches = []

    for index, row in hellofresh_data.iterrows():
        print(f"\n\"{row['name']}\" ({index+1}/{len(hellofresh_data)}) (tf-idf method))\n_____________________________")

        tfidf_matches = find_probable_matches_tfidf(row['name'], ciqual_data, vectorizer, tfidf_matrix)
        display_matches(tfidf_matches)

        while True:
            user_input = input("Enter the number of the chosen match or 'a' to show image: ")

            if user_input.lower() == 'a':
                image_path = os.path.join(images_directory, f"{row['id']}.jpg")
                display_image(image_path)
            elif user_input.isdigit():
                chosen_match_index = int(user_input)
                if chosen_match_index == 0:
                    print("No suitable TF-IDF match. Trying Levenshtein method...")

                    print(f"\n\"{row['name']}\" ({index+1}/{len(hellofresh_data)}) (Levenshtein method))\n_____________________________")
                    levenshtein_matches = find_probable_matches_levenshtein(row['name'], ciqual_data)
                    display_matches(levenshtein_matches)
                    chosen_match_index = input("Enter the number of the chosen Levenshtein match or 'a' to show image: ")
                    if chosen_match_index.isdigit():
                        chosen_match_index = int(chosen_match_index)
                        if 0 < chosen_match_index <= len(levenshtein_matches):
                            chosen_match = levenshtein_matches.iloc[chosen_match_index - 1]
                            chosen_match_name = chosen_match['alim_nom_fr']
                            chosen_match_id = chosen_match['id']
                            break
                        elif chosen_match_index == 0:
                            print("No suitable Levenshtein match.")
                            chosen_match_name = 'Pas de correspondance'
                            chosen_match_id = ''
                            break
                        else:
                            print("Invalid number. Please try again.")
                    elif chosen_match_index.lower() == 'a':
                        image_path = os.path.join(images_directory, f"{row['id']}.jpg")
                        display_image(image_path)
                    else:
                        print("Invalid input. Please enter a number or 'i' to show image.")
                elif 0 < chosen_match_index <= len(tfidf_matches):
                    chosen_match = tfidf_matches.iloc[chosen_match_index - 1]
                    chosen_match_name = chosen_match['alim_nom_fr']
                    chosen_match_id = chosen_match['id']
                    break
                else:
                    print("Invalid number. Please try again.")
            else:
                print("Invalid input. Please enter a number or 'i' to show image.")

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
image_dir = f"/home/adrien/git/flavor_forest/hello_fresh/data/ingredients/" # This is an example path
matches_df = interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename, image_dir)
