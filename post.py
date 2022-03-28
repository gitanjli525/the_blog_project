from flask import Blueprint, render_template,session,request,redirect
import json,datetime
from datetime import datetime
from .database import Posts,Users,db,Comment

post = Blueprint("post",__name__,static_folder="static",template_folder="templates")

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]

@post.route("/post/<string:post_slug>",methods = ['GET'])
def post_route(post_slug):
    if 'user' in session and session['user'] is not None:
        params['log'] = 1
        params['user'] = session['user']
    else :
        params['log'] = 0

    post = Posts.query.join(Users, Users.id==Posts.user_id).add_columns(Users.username, Users.email,Posts.id,Posts.user_id, Posts.content,Posts.title,Posts.slug,Posts.tagline,Posts.img_file,Posts.date).filter(Posts.slug == post_slug).first()
    # comments = Comment.query.filter_by(post_id = post.id).all()
    comments = Comment.query.join(Users, Users.id==Comment.user_id).add_columns(Users.username,Comment.id, Comment.content,Comment.date).filter(Comment.post_id == post.id).all()
    
    # return "<h1> post.username <h1>"
    return render_template("post.html",post = post,params = params,comments = comments)

@post.route("/edit/<string:username>/<string:id>",methods = ['GET','POST'])
def edit(username,id):
    if ("user" in session and session['user'] == username): 
        params['log']=1
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            
            if int(id) == -1:
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

@post.route("/delete/<string:id>", methods= ['GET'])
def delete(id):
    
    if(params['log']):
        Posts.query.filter_by(id = id).delete()
        db.session.commit()
        redirect('/')
        
    return redirect('/dashboard')



