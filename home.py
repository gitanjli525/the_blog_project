from flask import Blueprint, render_template,session,request
import json
from .database import Posts,Users
from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,desc

home = Blueprint("home",__name__,static_folder="static",template_folder="templates")

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]

@home.route("/")
def home_def():
    print("Entered home")

    params['log']=0
    if ('user' in session): 
        params['log']=1
        
    start_token =0
    post = Posts.query\
    .join(Users, Users.id==Posts.user_id)\
    .add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).order_by(desc(Posts.date)).all()

    params['total_post'] = len(post)
    post = post[start_token:start_token+params['no_of_posts']]
    return render_template("index.html",params =params,posts = post,start_token=start_token)




@home.route("/<int:token>")
def home_page(token):
    start_token = token
    print ("token:", token)
    if ('user' in session ): 
        params['log']=1

    post = Posts.query\
    .join(Users, Users.id==Posts.user_id)\
    .add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).order_by(desc(Posts.date)).all()

    params['total_post'] = len(post)
    post = post[start_token:start_token+params['no_of_posts']]
    return render_template("index.html",params =params,posts = post,start_token=start_token)

