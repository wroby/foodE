import os
import requests

#API KEY

key = os.environ.get('API_KEY')


def get_macronutrients(recipe):
    if recipe == "cup_cakes":
        recipe = recipe.replace("cup_cakes","cupcakes")
    elif recipe == "french_fries":
        recipe = recipe.replace("french_fries","fries_french")
    elif recipe == "fried_rice":
        recipe = recipe.replace("fried_rice","rice_fried")
    elif recipe == "fried_calamari":
        recipe = recipe.replace("fried_calamari","calamari_fried")
    elif recipe == "hot_and_sour_soup":
        recipe = recipe.replace("hot_and_sour_soup","sour_soup")
    elif recipe == "hot_dog":
        recipe = recipe.replace("hot_dog","hotdog")
    elif recipe == "prime_rib":
        recipe = recipe.replace("prime_rib","rib_prime")
    response = requests.get(f"https://api.spoonacular.com/recipes/guessNutrition?apiKey={key}&title={recipe}")
    if response.status_code == 200:
        return response.json()


    else:
        print(response.status_code)
        return None
