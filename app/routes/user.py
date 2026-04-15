from flask import Flask, render_template, request, redirect, Blueprint, session, flash, get_template_attribute
from sqlalchemy import select
from database.db import db
from app.services.models import User
from app.services.models import Recipe

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if 'username' in session:
            profile_session = session['username']
            profile_user : User = User.query.filter_by(email=profile_session).first()
            session['name'] = profile_user.name
            if not profile_user.last_name == "":
                session['surname'] = profile_user.last_name
            else:
                if 'surname' in session:
                    session.pop('surname',None)

        return render_template('userpage.html')
    

@userpage_bp.route('/user/edit',methods = ['POST','GET'])
def edit():
    flash('Sorry! I have not yet implemented the edit path!',category='error')
    return render_template('userpage.html')


@userpage_bp.route('/user/recipes',methods = ['POST','GET'])
def recipes():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if not 'username' in session:
            flash('You need to log in to view your recipes!',category='error')
        else:
            try:
                user : User = db.session.execute(select(User).where(User.email==session['username'])).first()
                recipe_list = db.session.execute(select(Recipe.recipe_title).where(Recipe.user_id==user.id)).fetchall()
                if not recipe_list:
                    flash("I could not find any recipes!",category='error')
                else:                           
                    template_recipes = get_template_attribute('userpage.html', 'recipe_list')
                    return template_recipes(recipe_list)
            except AttributeError as err:
                flash("It seems you do not have any recipes!",category='error')
        return render_template('userpage.html')
    


    
def view():
    id = request.args.get('recipe_id', type = int)
    recipe = Recipe.query.get(id)
    if not recipe:
        return redirect('/')
    else:
        return render_template('viewrecipe.html', recipe=recipe)