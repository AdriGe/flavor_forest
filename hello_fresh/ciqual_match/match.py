import os
import pandas as pd
from Levenshtein import ratio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from gensim.models import KeyedVectors
from gensim.models.fasttext import load_facebook_model

def load_data(hellofresh_csv_path, ciqual_csv_path):
    try:
        hellofresh_data = pd.read_csv(hellofresh_csv_path, usecols=['id', 'name', 'category'])
        ciqual_data = pd.read_csv(ciqual_csv_path)
        return hellofresh_data, ciqual_data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None, None, str(e)


def find_probable_matches_levenshtein(ingredient, ciqual_data):
    print(ingredient)
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
    matches = ciqual_data.iloc[top_indices]
    matches['similarity'] = cosine_scores[0, top_indices]
    return matches[['alim_code', 'alim_nom_fr', 'similarity']].reset_index(drop=True)


def bert_embeddings(sentences, model, tokenizer):
    """ Generate BERT embeddings for a list of sentences. """
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state
    attention_mask = encoded_input['attention_mask']
    embeddings = embeddings * attention_mask.unsqueeze(-1)
    mask_sum = torch.clamp(attention_mask.sum(dim=1, keepdim=True), min=1e-9)
    return (embeddings.sum(dim=1) / mask_sum).numpy()


def find_probable_matches_bert(ingredient, ciqual_data, model, tokenizer):
    # Generate embeddings for the ingredient and all Ciqual food names
    ingredient_embedding = bert_embeddings([ingredient], model, tokenizer)
    ciqual_embeddings = bert_embeddings(ciqual_data['alim_nom_fr'].tolist(), model, tokenizer)

    # Compute cosine similarity scores
    cosine_scores = cosine_similarity(ingredient_embedding, ciqual_embeddings)

    # Get the top 20 matches
    top_indices = cosine_scores.argsort()[0][-20:][::-1]
    matches = ciqual_data.iloc[top_indices]
    matches['similarity'] = cosine_scores[0, top_indices]
    return matches[['alim_code', 'alim_nom_fr', 'similarity']].reset_index(drop=True)


def load_fasttext_model(fasttext_model_path):
    """ Load the pre-trained FastText model. """
    #model = KeyedVectors.load_word2vec_format(fasttext_model_path, binary=False)
    #return model
    model = load_facebook_model(fasttext_model_path)
    return model.wv


def sentence_embedding(sentence, model):
    """ Generate sentence embedding as the mean of word embeddings. """
    words = sentence.split()
    word_embeddings = [model[word] for word in words if word in model]
    if not word_embeddings:
        return np.zeros(model.vector_size)
    sentence_embedding = np.mean(word_embeddings, axis=0)
    return sentence_embedding


def find_probable_matches_word_embeddings(ingredient, ciqual_data, model):
    # Generate embeddings for the ingredient
    ingredient_embedding = sentence_embedding(ingredient, model)

    # Generate embeddings for each ciqual food name and compute cosine similarity
    similarities = []
    for food_name in ciqual_data['alim_nom_fr']:
        food_embedding = sentence_embedding(food_name, model)
        sim_score = cosine_similarity([ingredient_embedding], [food_embedding])[0][0]
        similarities.append(sim_score)

    ciqual_data['similarity'] = similarities
    probable_matches = ciqual_data.sort_values(by='similarity', ascending=False).head(20)
    return probable_matches[['alim_code', 'alim_nom_fr', 'similarity']]


def interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename, method='levenshtein', fasttext_model_path=None):
    hellofresh_data, ciqual_data = load_data(hellofresh_csv_path, ciqual_csv_path)
    if hellofresh_data is None or ciqual_data is None:
        return "Failed to load data."

    if method == 'tfidf':
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(ciqual_data['alim_nom_fr'].dropna().astype(str))
    elif method == 'bert':
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
    elif method == 'word_embeddings':
        if not fasttext_model_path:
            raise ValueError("FastText model path must be provided for word embeddings method.")
        model = load_fasttext_model(fasttext_model_path)
    
    matches = []

    for index, row in hellofresh_data.iterrows():
        if method == 'levenshtein':
            probable_matches = find_probable_matches_levenshtein(row['name'], ciqual_data)
        elif method == 'tfidf':
            probable_matches = find_probable_matches_tfidf(row['name'], ciqual_data, vectorizer, tfidf_matrix)
        elif method == 'bert':
            probable_matches = find_probable_matches_bert(row['name'], ciqual_data, model, tokenizer)
        elif method == 'word_embeddings':
            probable_matches = find_probable_matches_word_embeddings(row['name'], ciqual_data, model)
        else:
            raise ValueError("Unknown method. Choose 'levenshtein' or 'tfidf'.")

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
    

base_path = '~/git/flavor_forest/hello_fresh/ciqual_match/hellofresh_generic'
hellofresh_csv_path = f"{base_path}/generic_hellofresh_11.csv" # This is an example path
output_filename = f"match_{os.path.basename(hellofresh_csv_path)}" # This is an example path
ciqual_csv_path = f"{base_path}/../ciqual.csv" # This is an example path
fasttext_model_path = f"{base_path}/../../dependencies/fasttext_models/cc.fr.300.bin" # This is an example path

matches_df = interactive_matching(hellofresh_csv_path, ciqual_csv_path, output_filename, method='word_embeddings', fasttext_model_path=fasttext_model_path)
