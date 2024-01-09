import pandas as pd
from Levenshtein import ratio

# Define a function to load the HelloFresh ingredients CSV and the Ciqual CSV for matching
def load_data(hellofresh_csv_path, ciqual_csv_path):
    try:
        hellofresh_data = pd.read_csv(hellofresh_csv_path)
        ciqual_data = pd.read_csv(ciqual_csv_path)
        return hellofresh_data, ciqual_data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None, None, str(e)

# Define a function to find the top 20 most probable Ciqual matches for a HelloFresh ingredient
def find_probable_matches(ingredient, ciqual_data):
    # Calculate similarity scores using Levenshtein distance
    ciqual_data['similarity'] = ciqual_data['alim_nom_fr'].apply(lambda x: ratio(ingredient.lower(), x.lower()))
    
    # Sort the results by similarity score in descending order
    probable_matches = ciqual_data.sort_values(by='similarity', ascending=False).head(20)
    return probable_matches[['alim_code', 'alim_nom_fr', 'similarity']]


# Define a function to interactively match HelloFresh ingredients to Ciqual food names
def interactive_matching(hellofresh_csv_path, ciqual_csv_path):
    # Load the data
    hellofresh_data, ciqual_data = load_data(hellofresh_csv_path, ciqual_csv_path)
    if hellofresh_data is None or ciqual_data is None:
        return "Failed to load data."
    
    # Create an empty DataFrame to store the matches
    matches_df = pd.DataFrame(columns=['hellofresh_id', 'ciqual_alim_nom_fr'])
    
    # Iterate through each HelloFresh ingredient
    for index, row in hellofresh_data.iterrows():
        print(f"Processing ingredient {index+1}/{len(hellofresh_data)}: {row['name']}")
        
        # Find the 20 most probable Ciqual matches for the current ingredient
        probable_matches = find_probable_matches(row['name'], ciqual_data)
        
        # Display the matches for user selection
        for idx, match in probable_matches.iterrows():
            print(f"{idx}: {match['alim_nom_fr']}")
        
        # Ask the user to choose a match
        chosen_match_index = input("Enter the number of the chosen match: ")
        chosen_match = probable_matches.iloc[int(chosen_match_index)]
        
        # Add the chosen match to the matches DataFrame
        matches_df = matches_df.append({
            'hellofresh_id': row['id'],
            'ciqual_alim_nom_fr': chosen_match['alim_nom_fr']
        }, ignore_index=True)
        
        # Save the matches DataFrame to a CSV file after each match to prevent data loss
        matches_df.to_csv('/home/adrien/Desktop/match/matches.csv', index=False)
        
        print(f"Match saved. {len(hellofresh_data) - index - 1} ingredients left.")
    
    return matches_df

# Paths to the CSV files (placeholders, to be replaced with actual file paths)
hellofresh_csv_path = '/home/adrien/Desktop/match/hellofresh/hellofresh_1.csv' # This is an example path
ciqual_csv_path = '/home/adrien/Desktop/match/ciqual.csv' # This is an example path

# Call the interactive matching function (this will only run in an interactive Python environment)
matches_df = interactive_matching(hellofresh_csv_path, ciqual_csv_path)

# As we cannot run interactive scripts in this environment, the code above is commented out
# In an interactive Python environment, you can uncomment and run the above line

# Please note that the above function is a basic implementation and assumes the 'alim_nom_fr' column
# exists in the Ciqual CSV file. The matching logic is also quite basic and should be enhanced
# for better accuracy.
