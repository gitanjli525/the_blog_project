
from flask import Flask, render_template, request ,session,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime
from flask_mail import Mail

# local_server = True
with open('config.json','r') as c:
    params = json.load(c)["params"]
params["log"]=0

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

if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
    
db = SQLAlchemy(app)

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



@app.route("/<string:token>")
def home(token):
    print("Entered home")
    start_token = int(token)
    if ('user' in session and session['user'] == params['admin']): 
        params['log']=1
    post = Posts.query.filter_by().all()
    params['total_post'] = len(post)
    post = post[start_token:start_token+params['no_of_posts']]
    return render_template("index.html",params =params,posts = post,start_token=start_token)

@app.route("/")
def home_def():
    print("Entered home")

    if ('user' in session and session['user'] == params['admin']): 
        params['log']=1
    start_token =0
    post = Posts.query.filter_by().all()
    params['total_post'] = len(post)
    post = post[start_token:start_token+params['no_of_posts']]
    return render_template("index.html",params =params,posts = post,start_token=0)

@app.route("/about")
def about():
    name = "happpy"
    return render_template("about.html",params =params)

@app.route("/dashboard",methods = ['GET','POST'])
def dashboard():
    cred = ""

    if ('user' in session and session['user'] == params['admin']): 
        params['log']=1
    post = Posts.query.all()
    if ('user' in session and session['user'] == params['admin']):
        return render_template("dashboard.html",params = params,posts = post)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if(username == params['admin'] and userpass == params['admin_password']):
            #set the session variable
            session['user'] = username
            params["log"] =1
            return render_template("dashboard.html",params= params,posts = post)
        else :
            return render_template("login.html",params = params,cred = "Wrong credentials !!!!")
        
    else: 
        return render_template("login.html",params =params,cred=cred)    
    

@app.route("/post/<string:post_slug>",methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template("post.html",post = post,params = params)

@app.route("/edit/<string:id>",methods = ['GET','POST'])
def edit(id):
    if ('user' in session and session['user'] == params['admin']): 
        params['log']=1
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            
            if id == '0':
                post = Posts(title = box_title,slug = slug,date = datetime.now(),content= content,tagline= tline,img_file = img_file)
                db.session.add(post)
                db.session.commit()
                return redirect("/post/"+post.slug)

            else:
                post = Posts.query.filter_by(id=id).first()
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

        post = Posts.query.filter_by(id =id).first()
        return render_template("edit.html",params = params,post = post,id=id)

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
                recipients = [params['gmail-user']],
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
    return render_template("contact.html",params =params)

# @app.route("/<string:wrong_page>",methods = ['GET'])
# def wrong_page(wrong_page):
#     return render_template("index.html",params =params)


app.run(debug = True)