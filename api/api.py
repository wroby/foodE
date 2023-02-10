import os
import requests

#params
recipe = os.environ.get('PREDICTION')
#possible querys
#API KEY
key = os.environ.get('API_KEY')

#Get complex search
#URL = "https://api.spoonacular.com/recipes/complexSearch?"

#Get findByNutrients
#URL = "https://api.spoonacular.com/recipes/findByNutrients"

def get_recipe_instructions(recipe):
    url = f"https://api.spoonacular.com/{recipe}/complexSearch?/{key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
