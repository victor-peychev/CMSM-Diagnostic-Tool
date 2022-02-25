from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
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
    phantom_scratching = SelectField("Phantom Sctratching", choices=['None', 'Phantom Scratching', 'Vocalization during phantom scratching'], validators=[DataRequired()])
    scratching_behind_head_or_ears = SelectField("Scratching and / or rubbing head or ears ", choices=['No', 'Yes'], validators=[DataRequired()])
    vocalization = SelectMultipleField("Vocalization", choices=[('1', 'Spontaneous yelping  or when changing position when recumbent '), ('2','Postural'), ('3', 'Defecation'), ('4', 'Any vocalization')])
    spinal_pain = SelectMultipleField("Spinal Pain", choices=['None', 'Cervical', 'Thoracolumar', 'Lumbosarcal', 'Any spinal pain'])
    activity = SelectField("Activity", choices=['None', 'Reduced exercise', 'Lethargy', 'Both (lethargic and reduced exercise)', 'Any activity change'])
    stairs_jumping = SelectField("Stairs/ Jumping", choices=['No', 'Yes'], validators=[DataRequired()])
    behavior_change = SelectMultipleField("Behavior Change", choices=['Greeting', 'Aggression', 'Timid / Anxious', 'Wtihdrawn', 'Any behavior change'])
    sleep = SelectField("Sleep disruption", choices=['No', 'Yes'], validators=[DataRequired()])
    other_pain_behaviors = SelectMultipleField("Other Pain Behaviors", choices=['Touch / grooming  aversion ears / head and/or neck', 'Touch / grooming aversion 1-2  limb and /paw ', 'touch / grooming aversion sternum or flank', 'Abnormal awake Head / neck posture', 'Sleeping elevated or unusual head posture', 'Squinting / Avoiding light', 'Licking limb /   paw', 'Pain face', '1 or more pain behaviors / signs' ])
    possibly_unrelated_behavior = SelectMultipleField("Possibly Unrelated Behavior", choices=['Repetitive tongue licking', 'Repetitive barking'])
    neurological_abnormalities = SelectMultipleField("Neurological Abnormalities", choices=['Weakness', 'Muscle atrophy', 'Postural responses decreased', 'Ataxia', 'Hypermetria', 'Scoliosis / cervicothoracic torticollis', 'Any neurological abnormality'])
    submit = SubmitField("Submit")


@app.route('/form', methods=['GET', 'POST'])
def form():
    vocalization = ''
    form = Form()
    if form.validate_on_submit():
        phantom_scratching = form.phantom_scratching.data
        form.phantom_scratching.data = ''
    return render_template("form.html",
    form = form )

