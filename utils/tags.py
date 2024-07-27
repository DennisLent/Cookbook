# dictionary to associate words for tags
tags_dict = {
    "Beef": ["beef", "steak", "ground beef", "mince beef"],
    "Chicken": ["chicken", "thighs", "wings", "breast"],
    "Pork": ["pork", "bacon", "ham", "pancetta", "guanciale"],
    "Fish": ["fish", "salmon", "tuna"],
    "Seafood": ["shrimp", "scampi", "lobster", "crab", "mussels"],
    "Pasta": ["pasta", "spaghetti", "linguini", "penne", "ravioli", "fusili", "tagliatelle", "tortellini", "farfalle", "macaroni", "gnocchi"],
    "Rice": ["rice", "basmati", "sushi", "arborio", "paella"]
}

def generate_tags(ingredients):
    dish_tags = set()

    # parse ingredients to search for tags
    combined_text = ingredients.lower()

    for tag, keywords in tags_dict.items():
        for keyword in keywords:
            if keyword in combined_text:
                dish_tags.add(tag)
    
    # check tags for animal, if there are non add vegetarian tag
    non_vegetarian = ["Beef", "Chicken", "Pork", "Fish", "Seafood"]
    vegetarian = True
    for animal_tag in non_vegetarian:
        if animal_tag in dish_tags:
            vegetarian = False
    
    if vegetarian:
        dish_tags.add("Vegetarian")
    
    return ", ".join(dish_tags)

