from flask import Flask, render_template, request, redirect, Blueprint, session
from database.db import db
from app.services.models import User
from app.services.models import Recipe

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        if 'username' in session: 
            profile_session = session['username']
            profile_user_id = User.query.filter_by(email=profile_session)
            user_recipes = Recipe.query.filter_by(user_id=profile_user_id)
        return redirect('/') # Nothing to post yet so... Back to homepage you go!    
    else:
        return render_template('userpage.html')