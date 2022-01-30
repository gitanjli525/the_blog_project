from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/happy")
def harry():
    name = "happpy"
    return render_template("about.html",name2 = name)

app.run(debug = True)