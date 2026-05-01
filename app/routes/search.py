from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import search

search_bp = Blueprint("searchpage", __name__)

#Page variables
page = 'searchpage.html'
path = '/search'
flashes = True

@search_bp.route('/search',methods = ['POST','GET'])
def searchpage():
    if request.method == "POST":
        try:
            pattern_filter: dict
            if getArgument(arguments=request.args, value="filter_recipe") == "on":
                pattern_filter["recipe"] = True
            else:
                pattern_filter["recipe"] = False

            if getArgument(arguments=request.args, value="filter_user") == "on":
                pattern_filter["user"] = True
            else:
                pattern_filter["user"] = False
            pattern: str = getArgument(arguments=request.args, value="pattern")

            results = search(pattern=pattern,filter=pattern_filter)
            return render_template(page,
                                search_recipes=pattern_filter["recipe"],
                                search_users=pattern_filter["user"],
                                result_users=results["users"],
                                result_recipes=results["recipes"])
        except Exception as error: return error
    else:
        return render_template(page)
    
def getArgument(arguments: dict, value: str):
    if hasArgument(arguments=arguments,value=value):
        return arguments.get(value)
    return None
    
def hasArgument(arguments: dict, value: str):
    if not arguments:
        return False
    if type(arguments.get(value)) == str:
        if arguments.get(value) == "":
            return False
    return True