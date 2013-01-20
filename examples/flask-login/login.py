from flask import Flask, redirect, render_template, request, url_for
from flask.ext.login import (AnonymousUser, LoginManager, UserMixin,
                             login_required, login_user, logout_user)
from flask.ext.simon import Simon
from simon import Model

app = Flask(__name__)
app.secret_key = 'Keep this value secret'
Simon(app)


login_manager = LoginManager()
login_manager.setup_app(app)


class Guest(AnonymousUser):
    """A basic guest user"""
login_manager.anonymous_user = Guest


class User(Model, UserMixin):
    """A basic user model, it hooks into Flask-Login using UserMixin"""

    def get_id(self):
        """Retrieves the documents ID

        This is required by Flask-Login
        """

        return getattr(self, 'id')

    def is_anonymous(self):
        """Checks if a user is not logged in

        This is required by Flask-Login
        """

        return 'id' not in self


@login_manager.user_loader
def load_user(id):
    """Loads the user for Flask-Login"""

    try:
        user = User.get(id=id)
    except User.NoDocumentFound:
        return None
    else:
        return user


@app.route('/')
def index():
    """Home page"""

    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Both prints the login form and logs in the user, redirects to the
    home page on success
    """

    errors = []

    if request.method == 'POST':
        # Check for a valid user on form submission
        try:
            # You'll want to do something better with password
            user = User.get(username=request.form.get('username'),
                            password=request.form.get('password'))
        except User.NoDocumentFound:
            # The combination wasn't found, show an error
            errors.append('The username and password were not found.')
        else:
            # Log in the user using Flask-Login
            login_user(user)
            return redirect(request.args.get('next') or url_for('.index'))

    return render_template('login.html', errors=errors)


@app.route('/logout')
@login_required
def logout():
    """Logs out the user, redirects to the home page"""

    logout_user()
    return redirect(url_for('.index'))
