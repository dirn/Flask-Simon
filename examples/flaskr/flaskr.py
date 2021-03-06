from flask import (Flask, request, session, redirect, url_for, abort,
                   render_template, flash)
from flask.ext.simon import Simon, Model


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
Simon(app)


class Entry(Model):
    class Meta:
        collection = 'entries'
        sort = '-id'


@app.route('/')
def show_entries():
    entries = Entry.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=('POST',))
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    Entry.create(title=request.form['title'], text=request.form['text'])
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
