from flask import Flask, render_template, request, redirect, Blueprint
from app.database.db import db
from app.database.tables import Recipe

#this creates a new blueprint to use
home_bp = Blueprint("home", __name__)

@home_bp.route('/', methods=['POST', 'GET'])
def home():
    recipe = Recipe.query.all()
    return render_template('homepage.html', recipies = recipe)
        