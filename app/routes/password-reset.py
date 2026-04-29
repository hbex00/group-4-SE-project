from flask import Flask, render_template, request, redirect, blueprints, session, flash
from database.db import db
from app.services.models import *
from app.utils.user import reset_password

passwordReset_bp = blueprints("password-reset", __name__)

@passwordReset_bp.route('/password-reset', methods=['POST', 'GET'])
def passwordReset():
    if 'id' in session:
        return redirect('/')
    
    if request.method == ('GET'):
        return render_template('password-reset.html')
    
    else:
        try:
            email = request.form['email']
            name = request.form['name']
            new_pass = request.form['password']
            user = User.query.filter_by(email=email,name=name).first()
            if user:
                new_user = reset_password(email, name, new_pass)
                if new_user == User:
                    session['id'] = new_user.id
                    session['first_name'] = new_user.name
                else:
                    "Error during password reset"
            else:
                return "Email and Name does not match"
        except:
            return 'Big Error'