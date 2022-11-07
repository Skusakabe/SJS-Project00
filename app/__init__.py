'''
Shinji, Jeffery, Sebastian
SoftDev
K<19> -- Login Session
<2022>-<11>-<3>
time spent: 2hrs
'''


from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import csv


'''

'''

DB_FILE = "website_information.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS account_information(username TEXT UNIQUE, password TEXT)")
c.execute("""CREATE TABLE IF NOT EXISTS story_list(storyname TEXT UNIQUE, tag TEXT, contributors TEXT, fullstory TEXT,
latestupdate TEXT, totalupdates INTEGER, latestcontributor TEXT, latestupdatetime TEXT)""")


app = Flask(__name__)    #create Flask object

app.secret_key = '77ad3ef4fbaf3d0cd0db350b92373f8aef6ec1843bffbef0626398d52be358cf'

@app.route("/")
def index():
    if 'username' in session:
        #go to main(response) page
        return redirect(url_for('home'))
    #go to login page
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login(): ## Maybe more methods will work in the /login root
    if request.method == 'POST':
        namepasslist = c.execute("SELECT * from account_information;").fetchall()
        names = [index[0] for index in namepasslist] #creates a list of just the names
        if request.form['username'] in names:
            if request.form['password'] == c.execute("SELECT password from account_information WHERE username = '" + request.form['username'] + "';").fetchone()[0]:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            return render_template('login.html', error = "Password is incorrect")
        return render_template('login.html', error = "Username does not exist")
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        namepasslist = c.execute("SELECT * from account_information;").fetchall()
        names = [index[0] for index in namepasslist] #creates a list of just the names
        if request.form['username'] not in names:
            if "|" not in request.form['password'] and len(request.form['password']) > 0:
                c.execute("INSERT INTO account_information VALUES ('" + request.form['username'] + "', '" + request.form['password'] + "');")
                return redirect(url_for('login'))
            return render_template('register.html', error = "Password contains invalid character '|' or is too short")
        return render_template('register.html', error = "Username already exists")            
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template( 'home.html' , username = session['username'])

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()