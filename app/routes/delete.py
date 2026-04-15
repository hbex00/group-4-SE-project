from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import Recipe

delete_bp = Blueprint("delete", __name__)

@delete_bp.route('/delete', methods=['POST', 'GET'])
def delete():
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.get(id)
    if request.method == 'POST':
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/')