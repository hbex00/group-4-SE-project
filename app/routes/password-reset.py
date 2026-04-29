from flask import Flask, render_template, request, redirect, blueprints, session, flash
from database.db import db
from app.services.models import *
from app.utils.user import reset_password
from app.utils.helper_function import session_handler

passwordReset_bp = blueprints("password-reset", __name__)

@passwordReset_bp.route('/password-eset', methods=['POST', 'GET'])
def passwordReset():
    if 'id' in session:
        return redirect('/')
    
    if request.method == ('GET'):
        return render_template('password-reset.html')
    
    else:
        try:
            email = request.form['email']
            name = request.form['name']
            new_pass = request.form['password1']
            password_control = request.form['password2']
            user = User.query.filter_by(email=email,name=name).first()
            if new_pass == password_control:
                if user:
                    new_user = reset_password(email, name, new_pass)
                    if new_user == User:
                        session_handler(new_user)
                        redirect('/')
                    else:
                        "Error during password reset"
                else:
                    return "Email and Name does not match"
            else:
                return "Password missmatch"
        except:
            return 'Big Error'