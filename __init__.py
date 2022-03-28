from flask import Flask, render_template, request ,session,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, join, func
from pprint import pprint
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime
from flask_mail import Mail
import sys, math,random

local_server = True
with open('config.json','r') as c:
    params = json.load(c)["params"]
params["log"]=0
forgot = {}

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)
db = SQLAlchemy(app)
if(True):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='example_user', password='password', server='67.205.144.13', database='tracebacks')

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://{user}:{password}@{server}/{database}'.format(user='example_user', password='password', server='67.205.144.13/phpmyadmin', database='tracebacks')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://example_user:password@67.205.144.13/tracebacks' 


class Contact (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(15), unique=True, nullable=False)
    msg = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Posts (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(80), nullable=True)
    slug = db.Column(db.String(21), unique=True, nullable=False)
    content = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True)
    img_file = db.Column(db.String(20), unique=False, nullable=True)
    user_id = db.Column(db.String(20), ForeignKey('users.id'), unique=False, nullable=True)

class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    pswd = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    about = db.Column(db.String(200), unique=True, nullable=False)

@app.route("/<string:token>")
def home(token):
    start_token = int(token)
    if ('user' in session ): 
        params['log']=1

    post = Posts.query\
    .join(Users, Users.id==Posts.user_id)\
    .add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).order_by(desc(Posts.date)).all()

    params['total_post'] = len(post)
    post = post[start_token:start_token+params['no_of_posts']]
    return render_template("index.html",params =params,posts = post,start_token=start_token)

@app.route("/")
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

@app.route("/about")
def about():
    
    if('user' not in session or session['user'] == None):
        return redirect("/dashboard")

    username = session['user']
    user = Users.query.filter_by(username = username).first()
    if(user == None):
        return redirect('/logout')
    post = Posts.query.join(Users, Users.id==Posts.user_id).add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).filter(Posts.user_id == user.id).all()

    return render_template("about.html",params =params,user = user,posts=post)

@app.route("/about/<string:username>")
def about_user(username):

    user = Users.query.filter_by(username = username).first()

    post = Posts.query.join(Users, Users.id==Posts.user_id).add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).filter(Posts.user_id == user.id).all()

    return render_template("about.html",params =params,user = user,posts=post)




@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    
    cred = ""
    # if (user_id in session and session[user_id] == user_id): 
    #     params['log']=1

    
    if ('user' in session and session['user'] != None):
        params['log'] = 1
        user = Users.query.filter_by(username = session['user']).first()
        if(user == None):
            return redirect('/logout')

        post = Posts.query.filter_by(user_id = user.id)
        return render_template("dashboard.html",params = params,posts = post,user = user)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        all_user = Users.query.filter_by(username = username).first()
        print('This is standard output',all_user, file=sys.stdout)

        if( all_user == None):
            return render_template("login.html",params = params,cred = "User Doesn't Exists !!!!")

        
        if(username == all_user.username and userpass == all_user.pswd ):
            #set the session variable
            session['user'] = username
            params["log"] =1
            post = Posts.query.filter_by(user_id = all_user.id)
            return render_template("dashboard.html",params= params,posts = post,user = all_user)
        else :
            return render_template("login.html",params = params,cred = "Wrong credentials !!!!")
        
    else: 
        return render_template("login.html",params =params,cred=cred)    
    

@app.route("/post/<string:post_slug>",methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template("post.html",post = post,params = params)

@app.route("/edit/<string:username>/<string:id>",methods = ['GET','POST'])
def edit(username,id):
    if ("user" in session and session['user'] == username): 
        params['log']=1
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            
            if int(id) == '-1':
                user_id  = Users.query.filter_by(username = username).first().id
                post = Posts(title = box_title,user_id = user_id ,slug = slug,date = datetime.now(),content= content,tagline= tline,img_file = img_file)
                db.session.add(post)
                db.session.commit()
                return redirect("/post/"+post.slug)

            else:
                post = Posts.query.filter_by(id=int(id)).first()
                if(box_title):
                    post.title = box_title
                if(slug):
                    post.slug = slug
                if(content):
                     post.content= content
                if(tline):
                    post.tagline= tline
                if(img_file):
                    post.img_file = img_file
                db.session.commit()
                session['user'] = None
                params["log"]=0                                                                          
                return redirect("/post/"+post.slug)
        user_id  = Users.query.filter_by(username = username).first().id
        post = Posts.query.filter_by(id = id,user_id=user_id).first()
        return render_template("edit.html",params = params,post = post,username=username,  id=id)

    else:
        return redirect("/dashboard")



@app.route("/contact", methods= ['GET','POST'])
def contact():
    print("Contact API is called")
    if(request.method == 'POST'):
        # add entry to the database
        name  = request.form.get('name')
        email  = request.form.get('email')
        phone  = request.form.get('phone')
        message  = request.form.get('message')

        entry = Contact(name = name, phone_num = phone,msg = message,email = email,date = datetime.now())
        print(entry)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("New message from " + name, 
                sender = email, 
                recipients = [params['gmail-user'],"abhishekkumar260ak@gmail.com"],
                body = message + '\n' + phone
                 )

    print("going to contact page")
    return render_template("contact.html",params =params)

@app.route("/logout", methods= ['GET'])
def logout():
    session.pop('user')
    params['log'] = 0
    return redirect('/')

@app.route("/delete/<string:id>", methods= ['GET'])
def delete(id):
    
    if(params['log']):
        Posts.query.filter_by(id = id).delete()
        db.session.commit()
        redirect('/')
        
    return redirect('/dashboard')

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

@app.route("/dp", methods= ['GET','POST'])
def dp_uploader():
  
    if(params['log']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(str(session['user'])+".jpg")))
            return redirect("/about/"+session['user'])       

    print("going to contact page")
    return render_template("/dashboard",params =params)


@app.route("/forgot", methods= ['GET','POST'])
def forgot_password():
    # print("Contact API is called")
    if request.method == 'POST':
        otp = generateOTP()
        email = request.form.get('uname')
        user = Users.query.filter_by(username = email).first()
        if(user == None):
            return render_template("reset.html",params =params,cred = "User Not Found!!")
        user.pswd = otp
        db.session.commit()
        cred = "Check Your mail and Enter your new Password"
        mail.send_message("New message from " + "Admin", 
                sender = 'admin@blogpost.com', 
                recipients = [user.email],
                body = "Your new password is : "+ otp +". Contact Admin if you haven't initiated this"
                 )
        return render_template("login.html",params =params,cred=cred)         
    
    return render_template("reset.html",params =params)

@app.route("/signup", methods= ['GET','POST'])
def signup():
    # print("Contact API is called")
    if request.method == 'POST':
        otp = generateOTP()
        uname = request.form.get('uname')
        email = request.form.get('email')
        user = Users.query.filter_by(username = uname).first()
        if(user):
            return render_template("signup.html",params =params,cred = "User_name not available!")

        about = request.form.get('about')
        name = request.form.get('name')

        new_user = Users(username = uname,about = about,Name=name,email =email,pswd = otp)
        db.session.add(new_user)
        db.session.commit()

        cred = "Check Your mail and Enter your new Password"
        mail.send_message("Welcome to Blog Commmunity " + uname, 
                sender = 'admin@blogpost.com', 
                recipients = [email],
                body = "Your new password is : "+ otp +". Contact Admin if you haven't initiated this"
                 )
        return render_template("login.html",params =params,cred="User credentials sent on mail.")         
    
    return render_template("signup.html",params =params)

def generateOTP() :

    digits = "0123456789"
    OTP = ""

    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP
    
app.run(debug = True)