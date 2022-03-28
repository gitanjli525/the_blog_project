from flask_sqlalchemy import SQLAlchemy
from .extension import db
from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,desc

class Contact (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(15), unique=True, nullable=False)
    msg = db.Column(db.String(200), unique=True, nullable=False)
    date = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String(200), unique=False, nullable=False)
    user_id = db.Column(db.String(20), ForeignKey('users.id'), unique=False, nullable=True)
    post_id = db.Column(db.String(20), ForeignKey('posts.id'), unique=False, nullable=True)
    date = db.Column(db.String(20), unique=True, nullable=True)


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

