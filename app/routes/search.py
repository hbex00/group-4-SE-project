from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.utils.search_db import text_search_table
from app.services.models import User,Recipe

search_bp = Blueprint("searchpage", __name__)

#Page Constants
PAGE = 'searchpage.html'
PATH = '/search'
FLASHES = True
FILTERS = {
    "Recipe": { # Class name, case sensitive
        "Time":[
            "15 minutes",
            "30 minutes",
            "45 minutes",
            "1 hour",
            "2 hours"],
        "Complexity":[
            "Easy",
            "Medium",
            "Hard",
            "GR"],
        "Spice":[
            "1",
            "2",
            "3"]
        },
    "User":{}
}

@search_bp.route('/search',methods = ['POST','GET'])
def searchpage():
    if request.method == "POST":
        try:
            pattern = getArgument(arguments=request.form.to_dict(), value="pattern")
            has_filter_user   = hasArgument(arg=request.form.to_dict(), val="")
            has_filter_recipe = hasArgument(arg=request.form.to_dict(), val="filter_recipe")
            has_any_filter    = has_filter_user | has_filter_recipe

            '''information_provided = request.form.listvalues()
            print(str(information_provided))
            information_provided = request.form.to_dict()
            print(str(information_provided))
            information_provided = request.form.getlist("types")
            print(str(information_provided))'''

            results = {}
            for search_class in request.form.getlist("types"):
                filterclass = f"{str(search_class)}_%"
                replace_string = f"{str(search_class)}_"
                print(str(filterclass))
                print(str(request.form.lists()))
                class_tags = {}
                
                for tag_type, tag_content in request.form.lists():
                    if replace_string in tag_type:
                        print("entered: "+str(tag_type))
                        tag_name = tag_type.replace(replace_string,"")
                        tag_list = {tag_name:tag_content}
                        class_tags.update(tag_list)
                print(str(class_tags))

                if class_tags:
                    print("CLASS TAGS::>>")
                    class_search_results = {search_class:text_search_table(pattern,search_class,class_tags)}
                
                else:
                    print("NO!! CLASS TAGS::>>")
                    class_search_results = {search_class:text_search_table(pattern,search_class)}
                
                results.update(class_search_results)
                
            '''if pattern:
                result_users = list()
                result_recipes = list()



                if has_filter_user:
                    result_users.extend(text_search_table(pattern,User,user_tags))
                    has_filter = False

                if has_filter_recipe | (not has_any_filter):
                    result_recipes.extend(text_search_table(pattern,Recipe,recipe_tags))
                    has_filter = True
                
                return render_template(PAGE,
                                    search_recipes=(not has_any_filter)|has_filter_recipe,
                                    search_users=has_filter_user,
                                    result_users=result_users,
                                    result_recipes=result_recipes)
            else:'''
            return render_template(PAGE,
                                search_recipes=(not has_any_filter)|has_filter_recipe,
                                search_users=has_filter_user)
            
        except Exception as error: return error
    else:
        return render_template(PAGE,filters=FILTERS)
    
def getArgument(arguments: dict, value: str):
    if hasArgument(arg=arguments,val=value):
        return arguments.get(value)
    return None
    
def hasArgument(arg: dict, val):
    if bool(arg) == False:
        return False
    if arg.get(val) == None:
        return False
    if type(arg.get(val)) == str and arg.get(val) == "":
        return False
    return True