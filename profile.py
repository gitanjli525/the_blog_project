from flask import Blueprint, render_template,session,request,redirect
from werkzeug.utils import secure_filename
import os ,json
# from extension import app

profile = Blueprint("profile",__name__,static_folder="static",template_folder="templates")

with open('config.json','r') as c:
    params = json.load(c)["params"]



