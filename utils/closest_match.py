import re

# List of common measurements
units = [
    'cup', 'cups', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp', 
    'ounce', 'ounces', 'oz', 'pound', 'pounds', 'lb', 'liter', 'l', 'liters', 'ml', 'milliliter', 
    'milliliters', 'gram', 'grams', 'g', 'kg', 'kilogram', 'kilograms', 'quart', 'quarts', 
    'pint', 'pints', 'gallon', 'gallons', 'package', 'packages', 'can', 'cans', 'bottle', 
    'bottles', 'slice', 'slices', 'clove', 'cloves', 'piece', 'pieces', 'stick', 'sticks',
    'dash', 'pinch', 'glass', 'bunch'
]

units_pattern = '|'.join(units)

def clean_ingredient(ingredient):
    # Remove quantity and unit
    ingredient = re.sub(r'\b\d+(\.\d+)?\s*(' + units_pattern + r')\b', '', ingredient)
    # Remove numbers
    ingredient = re.sub(r'\b\d+\b', '', ingredient)
    # Remove 'of'
    ingredient = re.sub(r'\bof\b', '', ingredient, flags=re.IGNORECASE)
    # Remove text within parentheses and tilde symbol
    ingredient = re.sub(r'\(.*?\)', '', ingredient)
    ingredient = ingredient.replace('~', '').replace('-', '').replace("/", "").replace("–", "")
    # Remove trailing 's'
    ingredient = re.sub(r'\bs\b', '', ingredient)
    # Remove extra whitespace
    ingredient = re.sub(r'\s+', ' ', ingredient).strip()
    return ingredient.lower()


def closest_match(input_ingredients, recipes):
    all_recipes = dict()
    recipe_matches = []
    for recipe in recipes:
        separated_ingredients = recipe["ingredients"].replace("\r", "").split("\n")
        cleaned_ingredients = [clean_ingredient(ingredient.lower()) for ingredient in separated_ingredients]
        all_recipes[recipe["id"]] = [recipe["title"], cleaned_ingredients]
    
    cleaned_input_ingredients = input_ingredients[0].replace("\r", "").split("\n")
    
    for recipe_id, title_ingredients in all_recipes.items():
        match_count = sum(1 for ing in cleaned_input_ingredients if any(ing in recipe_ing for recipe_ing in title_ingredients[1]))
        match_percentage = (match_count / len(title_ingredients[1])) * 100

        recipe_matches.append({
            'id': recipe_id,
            'title': title_ingredients[0],
            'match_percentage': match_percentage
        })

    recipe_matches = sorted(recipe_matches, key=lambda x: x['match_percentage'], reverse=True)
    if all(recipe['match_percentage'] == 0.0 for recipe in recipe_matches):
        return None
    
    return recipe_matches[:5]
