from flask import Blueprint, render_template,session,request,redirect
from .database import Posts,Users,db
from .extension import mail
from flask_mail import Mail
import math, random,json,sys

auth = Blueprint("auth",__name__,static_folder="static",template_folder="templates")

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]
    
@auth.route("/logout", methods= ['GET'])
def logout():
    session.pop('user')
    params['log'] = 0
    return redirect('/')

@auth.route("/forgot", methods= ['GET','POST'])
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

@auth.route("/dashboard",methods = ['GET','POST'])
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


@auth.route("/signup", methods= ['GET','POST'])
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