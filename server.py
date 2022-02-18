from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

@app.route('/')

def index():
    return render_template("home.html")

@app.route('/what_is_cm')

def what_is_cm():
    return render_template("what_is_cm.html")

@app.route('/website_purpose')

def website_purpose():
    return render_template("website_purpose.html")

@app.route('/base')

def base():
    return render_template("base.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

# Form class
class Form(FlaskForm):
    test = StringField("Test", validators=[DataRequired()])
    test1 = SelectField("Test1", choices=['Yes', 'No'], validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/form', methods=['GET', 'POST'])
def form():
    test = None
    test1 = None
    form = Form()
    if form.validate_on_submit():
        test = form.test.data
        form.test.data = ''
    return render_template("form.html",
    test = test,
    test1= test1,
    form = form )

