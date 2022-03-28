from flask import Blueprint, render_template,session,request,redirect
from werkzeug.utils import secure_filename
from .database import Comment,Posts,Users
from .extension import db
import datetime
from datetime import datetime
import os ,json
# from extension import app

comment = Blueprint("comment",__name__,static_folder="static",template_folder="templates")

with open('/var/www/blog_project/blog_project/config.json','r') as c:
    params = json.load(c)["params"]


@comment.route("/comment/<string:username>/<int:post_id>", methods= ['GET','POST'])
def add_comment(username,post_id):
    # print("Contact API is called")
    if(request.method == 'POST'):
        # add entry to the database
        content  = request.form.get('content')
        slug = Posts.query.filter_by(id = post_id).first().slug
        user_id = Users.query.filter_by(username= username).first().id

        entry = Comment(content = content,user_id = user_id,post_id = post_id, date = datetime.now())
        
      
        db.session.add(entry)
        db.session.commit()

        return redirect('/post/'+slug)
        
    return redirect("/")

