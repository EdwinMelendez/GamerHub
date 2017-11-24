from flask import Flask, request, redirect, render_template, url_for, session
import Models
from Forms import SignupForm, LoginForm
from Logger import Logger
from flask_login import login_user, logout_user, LoginManager, login_required


app = Flask(__name__)
logger = Logger()
# secret key & sqlalchemy database path
app.secret_key = 'tiniest little secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/gamerhub.sqlite'
# disabled this to not get sqlalchemy track modification errors
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# login manager handles login validation and current logged in user
login_manager = LoginManager()
login_manager.init_app(app)
# for debugging
app.debug = True
# create database
def init_db():
    Models.db.init_app(app)
    Models.db.app = app
    Models.db.create_all()


@app.route('/protected')
@login_required
def protected():
    return "protected area"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    # setting up flask form
    register_form = SignupForm()

    if request.method == 'GET':
        return render_template('register.html', form=register_form)

    elif request.method == 'POST':

        if register_form.validate_on_submit():
            if Models.db.session.query(Models.User).filter_by(username=register_form.username.data).first():
                return "User already exists"
            else:
                # create new user
                new_user = Models.User(register_form.username.data, register_form.password.data,
                                       register_form.email.data)
                Models.db.session.add(new_user)
                Models.db.session.commit()
                session['username'] = new_user.username
                login_user(new_user)

                # adding user to session

                return redirect(url_for('dashboard'))
        else:
            return "Form didn't validate"
        # redirects to dashboard
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=login_form)

    # login form
    elif request.method == 'POST':

        if login_form.validate_on_submit():

            user = Models.User.query.filter_by(username=login_form.username.data).first()

            if user:
                if user.password == login_form.password.data:
                    login_user(user)
                    session['username'] = user.username
                    return redirect(url_for('dashboard'))
                else:
                    return "Incorrect Password or Username"
            else:
                return "User doesn't exist"
        else:
            return "form not validated"

    # redirects to dashboard route

    return render_template('login.html')

# todo: route for profile page
# todo: route for keyword search result list with clickable titles/google image api
# todo: dynamic route for clicked result/game api display
# todo: route for homepage/dashboard

if __name__ == '__main__':
    init_db()
    app.run()
