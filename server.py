import json
from email.policy import default
from msilib.schema import CheckBox
from wsgiref.validate import validator
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_wtf import FlaskForm, Form
from sqlalchemy import ForeignKey
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

    # Create a one to many relationship with Sumbissions
    sumbission = db.relationship('Submissions', backref='user')

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


# Create Form Submissions Model
class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to users
    foreign_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    dogs_name = db.Column(db.String(128), nullable=False)
    dogs_breed = db.Column(db.String(128), nullable=False)
    dogs_dob = db.Column(db.Date, nullable=False)
    dogs_sex = db.Column(db.String(128), nullable=False)
    dogs_neutered = db.Column(db.String(128), nullable=False)
    scratching = db.Column(db.String(256), nullable=False)
    scratching_site_face_mouth = db.Column(db.String(256))
    scratching_site_ear_back_of_ear = db.Column(db.String(256))
    scratching_site_towards_neck_shoulder_with_left_back_foot = db.Column(db.String(256))
    scratching_site_towards_neck_shoulder_with_tight_back_foot = db.Column(db.String(256))
    scratching_site_chest = db.Column(db.String(256))
    scratching_site_tail_head = db.Column(db.String(256))
    scratching_site_belly = db.Column(db.String(256))
    scratching_triggers_rubbing_neck_chest_shoulder = db.Column(db.String(256))
    scratching_triggers_rubbing_belly = db.Column(db.String(256))
    scratching_triggers_rubbing_tailhead = db.Column(db.String(256))
    scratching_triggers_when_excited_anxious = db.Column(db.String(256))
    scratching_triggers_during_night = db.Column(db.String(256))
    vocalising_when_scratching_shoulder_neck = db.Column(db.String(256))
    vocalising_when_scratching_back_of_head_ear = db.Column(db.String(256))
    nibbling_licking_fore_feet = db.Column(db.String(256))
    nibbling_licking_hind_feet = db.Column(db.String(256))
    nibbling_licking_tail_head = db.Column(db.String(256))
    nibbling_licking_belly = db.Column(db.String(256))
    nibbling_licking_flank = db.Column(db.String(256))
    vocalisation_during_sleep = db.Column(db.String(256))
    vocalisation_on_rising_or_when_jumping = db.Column(db.String(256))
    vocalisation_when_being_picked_up = db.Column(db.String(256))
    vocalisation_during_defecation = db.Column(db.String(256))
    vocalisation_when_emotionally_aroused = db.Column(db.String(256))
    vocalisation_yelping_or_screaming_when_anxious = db.Column(db.String(256))
    vocalisation_yelping_or_screaming_text_box = db.Column(db.String(512))
    exercise = db.Column(db.String(256), nullable=False)
    play = db.Column(db.String(256), nullable=False)
    upstairs = db.Column(db.String(256), nullable=False)
    downstairs = db.Column(db.String(256), nullable=False)
    jumping = db.Column(db.String(256), nullable=False)
    interactions_no_longer_jumping_up_to_greet = db.Column(db.String(256))
    interactions_increase_in_anxious_behaviour = db.Column(db.String(256))
    interactions_more_withdraw = db.Column(db.String(256))
    interactions_more_timid_with_other_dogs_or_humans = db.Column(db.String(256))
    interactions_increased_agression_to_other_dogs = db.Column(db.String(256))
    interactions_growling_when_picked_up = db.Column(db.String(256))
    interactions_increased_agression_to_humans = db.Column(db.String(256))
    interactions_text_box = db.Column(db.String(512))
    sleep = db.Column(db.String(256), nullable=False)
    other_signs_tocuh_grooming_aversion_ears_head_and_or_neck = db.Column(db.String(256))
    other_signs_tocuh_grooming_aversion_1_2_limb_and_paw = db.Column(db.String(256))
    other_signs_tocuh_grooming_aversion_sternum_or_flank = db.Column(db.String(256))
    other_signs_abnormal_awake_head_neck_posture = db.Column(db.String(256))
    other_signs_sleeping_elevated_or_unusual_head_posture = db.Column(db.String(256))
    other_signs_squinting_avoiding_light = db.Column(db.String(256))
    other_signs_licking_limb_paw = db.Column(db.String(256))
    other_signs_pain_grimace = db.Column(db.String(256))



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
                return redirect(url_for('form'))
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
    submissions = Submissions.query.order_by(Submissions.date_added)
    return render_template('dashboard.html', submissions = submissions)


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

# Multicheckbox class

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Form class

class ToolForm(FlaskForm): # add date
    scratching = RadioField("Sctratching", choices=['No', 'Yes Occasional', 'Yes Frequent'], default = 'No', validators=[DataRequired()])
    scratching_site = MultiCheckboxField("Scratching site (tick all that apply)", choices=[('1','Face/ mouth'), ('2','Ear/ back of head'), ('3','Towards neck / shoulder with left back foot'), ('4','Towards neck / shoulder with right back foot'), ('5','Chest'), ('6','Tail head'), ('7','Belly')])
    scratching_triggers = MultiCheckboxField("Scratching triggers", choices=[('1','Rubbing of one area of skin (neck, chest, shoulder)'), ('2','Rubbing of one area of skin (belly)'), ('3','Rubbing of one area of skin (tailhead)'), ('4','When excited / anxious'), ('5','When walking on leash'), ('6','During night')])
    vocalising_when_scratching = MultiCheckboxField("Vocalising when scrathing", choices=[('1','Yes - Shoulder / neck  '), ('2','Yes - Back of head / ear')])
    nibbling_licking = MultiCheckboxField("Nibbling / licking", choices=[('1','Fore feet'), ('2','Hind feet'), ('3','Tail head'), ('4','Belly'), ('5','Flank')])
    vocalisation_yelping_or_screaming = MultiCheckboxField("Vocalisation (yelping or screaming)", choices=[('1','During sleep or when changing position when recumbent  '), ('2','On rising or when jumping'), ('3','When being picked up under sternum (by “armpits”)'), ('4','During defecation'), ('5','When emotionally aroused (for example seeing a squirrel)'), ('6','When anxious'), ('7','Other - please describe')])
    vocalisation_yelping_or_screaming_text_box = StringField()
    exercise = RadioField("Exercise", choices=[('1','Normal - pet is keen to exercise and shows no sign of fatigue during a 60-minute walk'), ('2','Reduced - pet is initially keen to exercise but will fatigue within 30-60 minutes'), ('3','Markedly reduced - pet refuses to exercise or will fatigue within 30 minutes')], default=1, validators=[DataRequired()])
    play = RadioField("Play", choices=[('1','Engages in play on a daily basis'), ('2','Engages in play 3-6 times a week'), ('3','Engages in play 1-3 times a week'), ('4','Rarely or does not engage in play')], default = '1', validators=[DataRequired()])
    upstairs = RadioField(choices=[('1','No hesitation / willing to go upstairs'), ('2','Hesitation / Unwilling to go upstairs')], default = '1', validators=[DataRequired()]) 
    downstairs = RadioField(choices=[('1','No hesitation / willing to go downstairs'), ('2','Hesitation / Unwilling to go downstairs')], default = '1', validators=[DataRequired()])
    jumping = RadioField(choices=[('1','No hesitation / willing to jump small heights'), ('2','Hesitation / unwilling to jump small heights'), ('3','Ability to jump small heights and or do stairs reduced to previously')], default = '1', validators=[DataRequired()]) 
    interactions = MultiCheckboxField("Interactions", choices=[('1','No longer jumping up to greet you on entry into the house'), ('2','Increase in anxious behaviour (lip licking, yawning, unable to settle, clinging, seeking reassurance)'), ('3','More withdraw'), ('4','More timid with other dogs or humans'), ('5','Increased aggression to other dogs'), ('6','Growling when picked up'), ('7','Increased aggression to humans'), ('8','Other behaviour change (open answer)') ])
    interactions_text_box = StringField()
    sleep = RadioField("Sleep", choices=[('1','Sleeps through the night / has undisrupted sleep'), ('2','Some sleep disturbance'), ('3','Does not sleep though the night / has disturbed sleep')], default = '1' , validators=[DataRequired()])
    other_signs = MultiCheckboxField("Other signs", choices=[('1','Touch / grooming  aversion ears / head and/or neck'), ('2','Touch / grooming aversion 1-2  limb and /paw '), ('3','touch / grooming aversion sternum or flank'), ('4','Abnormal awake Head / neck posture'), ('5','Sleeping elevated or unusual head posture'), ('6','Squinting / Avoiding light'), ('7','Licking limb /   paw'), ('8','Pain grimace')]) 
    # neurological_abnormalities = MultiCheckboxField("Neurological Abnormalities", choices=['Weakness', 'Muscle atrophy', 'Postural responses decreased', 'Ataxia', 'Hypermetria', 'Scoliosis / cervicothoracic torticollis', 'Any neurological abnormality (Not listed above)'])
    submit = SubmitField("Submit")


@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    form = ToolForm()

    if form.validate_on_submit():
        scratching_site = form.scratching_site.data
        scratching_triggers = form.scratching_triggers.data
        vocalising_when_scratching = form.vocalising_when_scratching.data
        nibbling_licking = form.nibbling_licking.data
        vocalisation_yelping_or_screaming = form.vocalisation_yelping_or_screaming.data
        interactions = form.interactions.data
        other_signs = form.other_signs.data

        submission = Submissions(foreign_id = current_user.id, dogs_name = current_user.dogs_name, dogs_breed = current_user.dogs_breed, dogs_dob = current_user.dogs_dob, dogs_sex = current_user.dogs_sex, dogs_neutered = current_user.dogs_neutered, scratching = form.scratching.data, scratching_site_face_mouth = process_array(scratching_site,'1'), scratching_site_ear_back_of_ear = process_array(scratching_site,'2'), scratching_site_towards_neck_shoulder_with_left_back_foot = process_array(scratching_site,'3'), scratching_site_towards_neck_shoulder_with_tight_back_foot = process_array(scratching_site,'4'), scratching_site_chest = process_array(scratching_site,'5'), scratching_site_tail_head = process_array(scratching_site,'6'), scratching_site_belly = process_array(scratching_site,'7'), scratching_triggers_rubbing_neck_chest_shoulder = process_array(scratching_triggers,'1'), scratching_triggers_rubbing_belly = process_array(scratching_triggers,'2'), scratching_triggers_rubbing_tailhead = process_array(scratching_triggers,'3'), scratching_triggers_when_excited_anxious = process_array(scratching_triggers,'4'), scratching_triggers_during_night = process_array(scratching_triggers,'5'),  vocalising_when_scratching_shoulder_neck = process_array(vocalising_when_scratching,'1'), vocalising_when_scratching_back_of_head_ear = process_array(vocalising_when_scratching,'2'), nibbling_licking_fore_feet = process_array(nibbling_licking,'1'), nibbling_licking_hind_feet = process_array(nibbling_licking,'2'), nibbling_licking_tail_head = process_array(nibbling_licking,'3'), nibbling_licking_belly = process_array(nibbling_licking,'4'), nibbling_licking_flank = process_array(nibbling_licking,'5'), vocalisation_during_sleep = process_array(vocalisation_yelping_or_screaming,'1'), vocalisation_on_rising_or_when_jumping = process_array(vocalisation_yelping_or_screaming,'2'), vocalisation_when_being_picked_up = process_array(vocalisation_yelping_or_screaming,'3'), vocalisation_during_defecation = process_array(vocalisation_yelping_or_screaming,'4'), vocalisation_when_emotionally_aroused = process_array(vocalisation_yelping_or_screaming,'5'), vocalisation_yelping_or_screaming_when_anxious = process_array(vocalisation_yelping_or_screaming,'6'), vocalisation_yelping_or_screaming_text_box = form.vocalisation_yelping_or_screaming_text_box.data, exercise = form.exercise.data, play = form.play.data, upstairs = form.upstairs.data, downstairs = form.downstairs.data, jumping = form.jumping.data, interactions_no_longer_jumping_up_to_greet = process_array(interactions,'1'), interactions_increase_in_anxious_behaviour = process_array(interactions,'2'), interactions_more_withdraw = process_array(interactions,'3'), interactions_more_timid_with_other_dogs_or_humans = process_array(interactions,'4'), interactions_increased_agression_to_other_dogs = process_array(interactions,'5'), interactions_growling_when_picked_up = process_array(interactions,'6'), interactions_increased_agression_to_humans = process_array(interactions,'7'), interactions_text_box = form.interactions_text_box.data, sleep = form.sleep.data, other_signs_tocuh_grooming_aversion_ears_head_and_or_neck = process_array(other_signs,'1'), other_signs_tocuh_grooming_aversion_1_2_limb_and_paw = process_array(other_signs,'2'), other_signs_tocuh_grooming_aversion_sternum_or_flank = process_array(other_signs,'3'), other_signs_abnormal_awake_head_neck_posture = process_array(other_signs,'4'), other_signs_sleeping_elevated_or_unusual_head_posture = process_array(other_signs,'5'), other_signs_squinting_avoiding_light = process_array(other_signs,'6'), other_signs_licking_limb_paw = process_array(other_signs,'7'), other_signs_pain_grimace = process_array(other_signs,'8'))
        db.session.add(submission)
        db.session.commit()
        flash("Submission added successfully ")
        return redirect(url_for('dashboard'))

    else:
        for error in form.errors:
            flash(error)

    form.scratching_site.data = ''
    form.scratching_triggers.data = ''
    form.vocalising_when_scratching.data = ''
    form.nibbling_licking.data = ''
    form.vocalisation_yelping_or_screaming.data = ''
    form.vocalisation_yelping_or_screaming_text_box.data = ''
    form.interactions.data = ''
    form.interactions_text_box.data = ''
    form.other_signs.data = ''
    all_submissions = Submissions.query.order_by(Submissions.date_added)
    return render_template("form.html", form = form, all_submissions= all_submissions )

def process_array(array, contains):
    if array is None:
        return '0'
    else:
        if contains in array:
            return '1'
        else:
           return '0'

