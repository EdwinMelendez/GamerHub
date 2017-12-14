from flask import Flask, request, render_template, session
import Models
from Forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, LoginManager, login_required
import GameDatabaseApi



app = Flask(__name__)
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

# holds global list of initially searched games
global_games = []

# protected area
@app.route('/protected')
@login_required
def protected():
    return "protected area"

# logout route
@app.route("/logout")
def logout():
    print('logging out user...')
    ''' session.clear() clears out logged session user, but breaks code while if user isn't logged in and tries to search'''
    session.clear()
    logout_user()
    return render_template('index.html')

# loads username into login manager
@login_manager.user_loader
def load_user(username):
    return Models.User.query.filter_by(user_name=username).first()

# index route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():

    # setting up flask form
    register_form = SignupForm()

    if request.method == 'GET':
        return render_template('register.html', form=register_form)

    elif request.method == 'POST':

        if register_form.validate_on_submit():
            if Models.db.session.query(Models.User).filter_by(user_name=register_form.username.data).first():
                return "User already exists"
            else:
                # create new user
                new_user = Models.User(register_form.username.data, register_form.password.data,
                                       register_form.email.data)
                Models.db.session.add(new_user)
                Models.db.session.commit()
                session['username'] = new_user.user_name
                login_user(new_user)
                # keeps track of if user is logged in
                logState = True

                # adding user to session

                return render_template('index.html', logState=logState)
        else:
            return "Form didn't validate"
        # redirects to dashboard
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # sets up flask login form
    login_form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=login_form)

    # login form
    elif request.method == 'POST':

        if login_form.validate_on_submit():

            user = Models.User.query.filter_by(user_name=login_form.username.data).first()

            if user:
                if user.password == login_form.password.data:
                    login_user(user)
                    session['username'] = user.user_name
                    logState = True
                    return render_template('index.html', logState=logState)
                else:
                    return "Incorrect Password or Username"
            else:
                return "User doesn't exist"
        else:
            return "form not validated"

    # redirects to dashboard route

    return render_template('login.html')



@app.route('/results', methods=['GET', 'POST'])

def results():

    if request.method == 'POST':
        # grabs search word
        search_words = (request.form['search'])

        # checks database if user had searched for game before, then adds to database if not
        if 'username' in session:
            c_user = session['username']
            logState = True

            if Models.Query.find_game(search_words):
                print('game already exists')

            else:
                new_search = Models.Tracked_Games(search_words, c_user)
                Models.db.session.add(new_search)
                Models.db.session.commit()

            # generates list of game object results
            result = GameDatabaseApi.generate_search_list(search_words)

            # if user didn't search a word it reroutes to error page
            if search_words == None:
                error = 'please try again'
                return render_template("searcherror.html", searched_word=search_words, logState=logState)

            else:
                # holds list of games, then pushes list of game names to global game list
                games = []
                for game in result.body:
                    game = game['name']
                    games.append(game)
                    global_games.append(game)

                return render_template("results.html", game=games, searched_word=search_words, logState=logState)


@app.route('/gameresults', methods=['GET', 'POST'])

def gameresults():

    if request.method == 'GET':

        return render_template('gameresults.html')

    if request.method == 'POST':
        logState = True
        value = request.form['game']

        '''depending on which game you select, this method matches
        the first instance of that same game resulting in the exact game you selected.
        then plugs that single game into the single search method, resulting in info
        about that single game.'''

        for n in global_games:
            if value == n:
                new_game = value

                result = GameDatabaseApi.single_search(new_game)

                info = []

                for n in result:
                    info.append(n)

                single_game = info.pop(0)

                for val in single_game.values():
                    print(val)

                game_name = single_game['name']

                if 'summary' not in single_game.keys():
                    summary = 'missing from database'
                else:
                    summary = single_game['summary']

                if 'rating' not in single_game.keys():
                    rating = 'missing from database'
                else:
                    rating = single_game['rating']

                if 'developers' not in single_game.keys():
                    developers = 'missing from database'
                else:
                    developers = single_game['developers'][0]['name']

                if 'genre' not in single_game.keys():
                    genre = 'missing from database'
                else:
                    genre = single_game['genres'][0]['name']

                if 'cover' not in single_game.keys():
                    cover_url = 'missing from database'
                else:
                    cover_url = single_game['cover']['url']

                if 'screenshots' not in single_game.keys():
                    screenshot_one = 'missing from database'
                    screenshot_two = 'missing from database'
                else:
                    screenshot_one = single_game['screenshots'][0]['url']
                    screenshot_two = single_game['screenshots'][1]['url']



                return render_template('gameresults.html', game_name=game_name, summary=summary, rating=rating,
                                       developers=developers, genre=genre, logState=logState, cover=cover_url, screenshot_one=screenshot_one,
                                       screenshot_two=screenshot_two)





@app.route('/searcherror', methods=['GET', 'POST'])
def searcherror():

    if request.method == 'GET':
        return render_template('searcherror.html')


if __name__ == '__main__':
    init_db()

    app.run(debug=True)
