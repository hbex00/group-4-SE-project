from flask import Flask, session
from sqlalchemy import select
from database.db import db
from app.services.models import *

def search(pattern, filter : dict):
    return_dict: dict
    return_users: list
    return_recipes: list
    if pattern is (None or ""):
        return_dict["users"] = None
        return_dict["recipes"] = None
        return return_dict
    
    if not filter is None:
        if filter.get('user') and filter.get('user') == True:
            for i in range(0,len(select(User))):
                user = db.session.get(User,i)
                fullname :str = (user.name + (user.last_name | "")).lower()
                if pattern in fullname:
                    return_users.append(user)    
            return_dict["users"] = return_users
        else:
            return_dict["users"] = None    

        if filter.get('recipe') and filter.get('recipe') == True:
            for i in range(0,len(select(Recipe))):
                recipe = db.session.get(Recipe,i)
                text :str = (recipe.recipe_title).lower() + ((recipe.description).lower() | "") + ((recipe.steps).lower() | "")
                if pattern in text:
                    return_recipes.append(recipe) 
            return_dict["recipes"] = return_recipes
        else:
            return_dict["recipes"] = None

    else: # Assuming recipe search based on missing filter argument -> Otherwise should be recipe == False
        for i in range(0,len(select(Recipe))):
            recipe = db.session.get(Recipe,i)
            text :str = (recipe.recipe_title).lower() + ((recipe.description).lower() | "") + ((recipe.steps).lower() | "")
            if pattern in text:
                return_recipes.append(recipe)
        if list(return_recipes).count == 0:
            return_recipes = None
        return_dict["recipes"] = return_recipes
        return_dict["users"] = None
    return return_dict

def fetch_users():
    return_users : dict
    for i in range(0,len(select(User))):
        return_users[i] = db.session.get(User,i)
    return return_users