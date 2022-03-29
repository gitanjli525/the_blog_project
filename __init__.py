from flask import Flask, render_template, request ,session,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, join, func
from pprint import pprint

import json,os
from werkzeug.utils import secure_filename

from datetime import datetime
from flask_mail import Mail

# ************ Blue Print*************
from .home import home
from .post import post 
from .auth import auth
from .about import about 
from .comment import comment 

# ***********Initialization************
from .extension import db,mail

app = Flask(__name__)

local_server = True
# with open('config.json','r') as c:
#     params = json.load(c)["params"]

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]
params["log"]=0
forgot = {}


# app.init_app(app)


app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail.init_app(app)
db.init_app(app)

app.register_blueprint(home,url_prefix="")
app.register_blueprint(comment,url_prefix="")
app.register_blueprint(auth,url_prefix="")
app.register_blueprint(post,url_prefix="")
app.register_blueprint(about,url_prefix="")

if(True):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]


@app.route("/dp", methods= ['GET','POST'])
def dp_uploader():
  
    if('user' in session and session['user'] is not None):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(str(session['user'])+".jpg")))
            return redirect("/about/"+session['user'])       

    print("going to contact page")
    return render_template("/dashboard",params =params)

@app.route("/uploader", methods= ['GET','POST'])
def uploader():
    print("Contact API is called")
    if(params['log']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return "Uploaded Successfully"        

    print("going to contact page")
    return render_template("/dashboard",params =params)


# app.run(debug = True)
