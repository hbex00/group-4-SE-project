from flask import Flask, render_template, request, redirect, Blueprint, session, flash, get_template_attribute
from sqlalchemy.orm import joinedload
from database.db import db
from app.services.models import User
from app.services.models import Recipe

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/') # Nothing Post-able added yet! To the homepage with thee!
    else:
        if 'id' in session:
            profile_id = session['id']
            profile_user : User = User.query.filter_by(id=profile_id).first()
            session['first_name'] = profile_user.name
            if not profile_user.last_name == "":
                session['last_name'] = profile_user.last_name
            else:
                session.pop('last_name',None)

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
        if not 'id' in session:
            flash('You need to log in to view your recipes!',category='error')
        else:
            try:
                user = User.query.get(session.get('id'))
                return render_template('userpage.html',user=user,show_recipes=True)
            except AttributeError as err:
                flash("Attribute Error!>" + str(err),category='error')
        return render_template('userpage.html')