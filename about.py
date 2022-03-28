from flask import Blueprint, render_template,session,request,redirect
from .database import Posts,Users,db,Contact
from .extension import mail
from flask_mail import Mail
import math, random,json

about = Blueprint("about",__name__,static_folder="static",template_folder="templates")

# with open('config.json','r') as c:
#     params = json.load(c)["params"]

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]


@about.route("/about")
def about_api():
    
    if('user' not in session or session['user'] == None):
        return redirect("/dashboard")

    params['log'] =1
    username = session['user']
    user = Users.query.filter_by(username = username).first()
    if(user == None):
        return redirect('/logout')
    post = Posts.query.join(Users, Users.id==Posts.user_id).add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).filter(Posts.user_id == user.id).all()

    return render_template("about.html",params =params,user = user,posts=post)

@about.route("/about/<string:username>")
def about_user(username):

    user = Users.query.filter_by(username = username).first()

    post = Posts.query.join(Users, Users.id==Posts.user_id).add_columns(Users.id, Users.username, Users.email, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).filter(Posts.user_id == user.id).all()

    return render_template("about.html",params =params,user = user,posts=post)
    



@about.route("/contact", methods= ['GET','POST'])
def contact():
    print("Contact API is called")
    if(request.method == 'POST'):
        # add entry to the database
        content  = request.form.get('content')
        

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