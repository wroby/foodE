import os
import requests

#params
recipe = os.environ.get('prediction')
#possible querys


#Get complex search
#URL = "https://api.spoonacular.com/recipes/complexSearch?"

#Get findByNutrients
#URL = "https://api.spoonacular.com/recipes/findByNutrients"

def get_recipe_instructions(recipe):
    url = f"https://api.spoonacular.com/{recipe}/complexSearch?"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
