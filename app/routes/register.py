from flask import Flask, render_template, request, redirect, Blueprint
from database.db import db
from app.services.models import *

register_bp = Blueprint("register", __name__)

@register_bp.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
    else:
        return render_template('registerpage.html')