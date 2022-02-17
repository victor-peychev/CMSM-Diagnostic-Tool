from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def index():
    return render_template("home.html")

@app.route('/base')

def base():
    return render_template("base.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
