from flask import Flask, render_template, request, redirect, Blueprint

userpage_bp = Blueprint("userpage", __name__)

@userpage_bp.route('/user',methods = ['POST','GET'])
def userpage():
    if request.method == 'POST':
        return redirect('/') # Nothing to post yet so... Back to homepage you go!    
    else:
        return render_template('userpage.html')