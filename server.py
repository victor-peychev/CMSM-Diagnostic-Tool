from wsgiref.validate import validator
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_wtf import FlaskForm, Form
from wtforms import widgets, DateField, PasswordField, BooleanField, ValidationError ,SubmitField, SelectField, SelectMultipleField, RadioField, FormField, StringField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#Flask instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1421@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = "secretkey"
#Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Users Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(128), nullable=False)
    dogs_name = db.Column(db.String(128), nullable=False)
    dogs_breed = db.Column(db.String(128), nullable=False)
    dogs_dob = db.Column(db.Date, nullable=False)
    dogs_sex = db.Column(db.String(128), nullable=False)
    dogs_neutered = db.Column(db.String(128), nullable=False)
    is_a_vet = db.Column(db.String(64), default='No')

    @property
    def password_hash(self):
        raise AttributeError('password is not a readable attribute')

    @password_hash.setter
    def password_hash(self,password_hash):
        self.password = generate_password_hash(password_hash)
    
    def verify_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


    # Create A String
    def __repr__(self):
        return '<Username %r>' % self.username

"""
# Create Forum Submissions Model
class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secondary_id = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    dogs_name = db.Column(db.String(128), nullable=False)
    dogs_breed = db.Column(db.String(128), nullable=False)
    dogs_name = db.Column(db.String(128), nullable=False)
    dogs_dob = db.Column(db.Date, nullable=False)
    dogs_sex = db.Column(db.String(128), nullable=False)
    dogs_neutered = db.Column(db.String(128), nullable=False)
    scratching = db.Column(db.String(128), nullable=False)
    scratching_site = db.Column(db.String(128), nullable=False)
    scratching_triggers = db.Column(db.String(128), nullable=False)
    vocalising_when_scratching = db.Column(db.String(128), nullable=False)
    nibbling_licking = db.Column(db.String(128), nullable=False)
    vocalisation_yelping_or_screaming = db.Column(db.String(128), nullable=False)
    vocalisation_yelping_or_screaming_text_box = db.Column(db.String(128), nullable=False)
    exercise = db.Column(db.String(128), nullable=False)
    play = db.Column(db.String(128), nullable=False)
    stairs_jumping = db.Column(db.String(128), nullable=False)
    interactions = db.Column(db.String(128), nullable=False)
    interactions_text_box = db.Column(db.String(128), nullable=False)
    sleep = db.Column(db.String(128), nullable=False)
    other_signs = db.Column(db.String(128), nullable=False)

"""


# Create Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hashed_password = generate_password_hash(form.password.data, "sha256")
            user = Users(username = form.username.data, email = form.email.data, password = hashed_password, dogs_name = form.dogs_name.data, dogs_breed = form.dogs_breed.data, dogs_dob = form.dogs_dob.data, dogs_sex = form.dogs_sex.data, dogs_neutered = form.dogs_neutered.data)
            db.session.add(user)
            db.session.commit()
            flash("User Registered")
        else:
            flash("User exists")
        username = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        form.dogs_name.data = ''
        form.dogs_breed.data = ''
        form.dogs_dob.data = ''
        form.dogs_sex.data = ''
        form.dogs_neutered.data = ''

    our_users = Users.query.order_by(Users.date_added)
    return render_template("register.html", form=form, username=username, our_users=our_users)

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check Hash
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again")
        else:
            flash("User doesnt exist Try Again")
    return render_template('login.html', form=form)


# Create Logout Function
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('login'))

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    username = None
    form = RegisterForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("register.html", form=form, username=username, our_users=our_users)

    except:
        flash("There was problem deleting user")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("register.html", form=form, username=username, our_users=our_users)

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

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2', message='Passwords mush match')])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    dogs_name = StringField("Dog's Name", validators=[DataRequired()])
    dogs_breed = StringField("Dogs' Breed", validators=[DataRequired()])
    dogs_dob = DateField("Dog's Date of Birth", validators=[DataRequired()])
    dogs_sex = RadioField("Dog's sex", choices=['Male', 'Female'], validators=[DataRequired()])
    dogs_neutered = RadioField("Is the dog neutered", choices=['Yes', 'No'], validators=[DataRequired()])
    submit = SubmitField("Submit")

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LoginForm(FlaskForm):
    # dog's name, dog's breed, dob, sex(neutered)
    # after diagnosis smn sms cmp
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sumbit')

# Form class

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class StairsJumping(Form):
    upstairs = RadioField(choices=['No hesitation / willing to go upstairs', 'Hesitation / Unwilling to go upstairs'], default = 'No hesitation / willing to go upstairs', validators=[DataRequired()]) 
    downstairs = RadioField(choices=['No hesitation / willing to go downstairs', 'Hesitation / Unwilling to go downstairs'], default = 'No hesitation / willing to go downstairs', validators=[DataRequired()])
    jumping = RadioField(choices=['No hesitation / willing to jump small heights', 'Hesitation / unwilling to jump small heights', 'Ability to jump small heights and or do stairs reduced to previously'], default = 'No hesitation / willing to jump small heights', validators=[DataRequired()]) 

class ToolForm(FlaskForm): # add date
    scratching = RadioField("Sctratching", choices=['No', 'Yes Occasional', 'Yes Frequent'], default = 'No', validators=[DataRequired()])
    scratching_site = MultiCheckboxField("Scratching site (tick all that apply)", choices=['Face/ mouth', 'Ear/ back of head', 'Towards neck / shoulder with left back foot', 'Towards neck / shoulder with right back foot', 'Chest', 'Tail head', 'Belly'])
    scratching_triggers = MultiCheckboxField("Scratching triggers", choices=['Rubbing of one area of skin (neck, chest, shoulder)', 'Rubbing of one area of skin (belly)', 'Rubbing of one area of skin (tailhead)', 'When excited / anxious', 'When walking on leash', 'During night', 'No trigger'])
    vocalising_when_scratching = MultiCheckboxField("Vocalising when scrathing", choices=['Yes - Shoulder / neck  ', 'Yes - Back of head / ear'])
    nibbling_licking = RadioField("Nibbling / licking", choices=['Fore feet', 'Hind feet', 'Tail head', 'Belly', 'Flank'])
    vocalisation_yelping_or_screaming = MultiCheckboxField("Vocalisation (yelping or screaming)", choices=['During sleep or when changing position when recumbent  ', 'On rising or when jumping', 'When being picked up under sternum (by “armpits”)', 'During defecation', 'When emotionally aroused (for example seeing a squirrel)', 'When anxious', 'Other - please describe'], validators=[DataRequired()])
    vocalisation_yelping_or_screaming_text_box = StringField()
    exercise = RadioField("Exercise", choices=['Normal - pet is keen to exercise and shows no sign of fatigue during a 60-minute walk', 'Reduced - pet is initially keen to exercise but will fatigue within 30-60 minutes', 'Markedly reduced - pet refuses to exercise or will fatigue within 30 minutes'], default='Normal - pet is keen to exercise and shows no sign of fatigue during a 60-minute walk', validators=[DataRequired()])
    play = RadioField("Play", choices=['Engages in play on a daily basis', 'Engages in play 3-6 times a week', 'Engages in play 1-3 times a week', 'Rarely or does not engage in play'], default = 'Engages in play on a daily basis', validators=[DataRequired()])
    stairs_jumping = FormField(StairsJumping)
    interactions = MultiCheckboxField("Interactions", choices=['No change', 'No longer jumping up to greet you on entry into the house', 'Increase in anxious behaviour (lip licking, yawning, unable to settle, clinging, seeking reassurance)', 'More withdraw', 'More timid with other dogs or humans', 'Increased aggression to other dogs', 'Growling when picked up', 'Increased aggression to humans', 'Other behaviour change (open answer)' ])
    interactions_text_box = StringField()
    sleep = RadioField("Sleep", choices=['Sleeps through the night / has undisrupted sleep', 'Does not sleep though the night / has disturbed sleep'], validators=[DataRequired()])
    other_signs = MultiCheckboxField("Other signs", choices=['Touch / grooming  aversion ears / head and/or neck', 'Touch / grooming aversion 1-2  limb and /paw ', 'touch / grooming aversion sternum or flank', 'Abnormal awake Head / neck posture', 'Sleeping elevated or unusual head posture', 'Squinting / Avoiding light', 'Licking limb /   paw', 'Pain grimace']) 
    # neurological_abnormalities = MultiCheckboxField("Neurological Abnormalities", choices=['Weakness', 'Muscle atrophy', 'Postural responses decreased', 'Ataxia', 'Hypermetria', 'Scoliosis / cervicothoracic torticollis', 'Any neurological abnormality (Not listed above)'])
    submit = SubmitField("Submit")


@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    form = ToolForm()
    #submission = Submissions(scratching = form.scratching.data, scratching_site = form.scratching_site.data, scratching_triggers = form.scratching_triggers.data, vocalising_when_scratching = form.vocalising_when_scratching.data, nibbling_licking = form.nibbling_licking.data, vocalisation_yelping_or_screaming = form.vocalisation_yelping_or_screaming.data, vocalisation_yelping_or_screaming_text_box = form.vocalisation_yelping_or_screaming_text_box.data, exercise = form.exercise.data, play = form.play.data, stairs_jumping = form.stairs_jumping.data, interactions = form.interactions.data, interactions_text_box = form.interactions_text_box.data, sleep = form.sleep.data, other_signs = form.other_signs.data)
    #db.session.add(submission)
    #db.session.commit()
    return render_template("form.html",
    form = form )

