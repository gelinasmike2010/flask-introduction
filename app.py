# import the Flask class from the flask module

from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

# create the application object
app = Flask(__name__)

#when using sessions, we need a secret key; this should be random
app.secret_key = "my precious"

# config to tell flask the database we're using
app.database = "sample.db"

# we write a function to be layered on top of basic site functions
# that nothing should go ahead unless user is logged in

# note: *args and **kwargs are used to allow for an unknown number of arguments
# these are a placeholder that allow the function to accept an arbitrry number of argyments

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

# at the index page, we run the login required function
# if user is not logged in => redirect to /login
@app.route('/')
@login_required
def home():
    # g is temporary Flask object that stores values, but is reset after a request
    g.db = connect_db()
    cur = g.db.execute('select * from posts')

    # if logged in, display the post history!
    # uses a list comprehension to grab all rows of the post table
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template at /welcome

# by default, funtions in Flask operate with the 'GET' method
# for login, we identify desired HTTP actions -- add POST to the default of GET

# redirect is a method that sends you to a new place
# url_for is a method that sends you to the function it takes as an argument

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True      # start a session if login successful
            flash('You are logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)      # on logout, pop the True value from the session
    flash('You are logged out.')
    return redirect(url_for('welcome'))

# this function
def connect_db():
    return sqlite3.connect(app.database)

# start the server with the 'run()' method in debug mode

if __name__ == '__main__':
    app.run(debug=True)
