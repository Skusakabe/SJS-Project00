'''
Shinji, Jeffery, Sebastian
SoftDev
P<00> -- Scenario 1
<2022>-<11>-<7>
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
latestupdate TEXT, totalupdates INTEGER)""") # maybe add a "latestupdatetime TEXT" to the table.


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
        if request.form['username'] not in names and "+" not in request.form['username']:
            if len(request.form['password']) > 0:
                newacc = [request.form['username'], request.form['password']]
                c.execute("INSERT INTO account_information VALUES (?, ?)", newacc)
                db.commit()
                return redirect(url_for('login'))
            return render_template('register.html', error = "Password is too short")
        return render_template('register.html', error = "Username already exists or contains invalid character '+'")            
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        h.append(titlelist[num])
        a.append(authorlist[num])
        s.append(storylist[num])
        num += 1
    return render_template('home.html', len = len(h), h = h, a = a, s = s, username = session['username'])

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        storyinfotable = c.execute("SELECT * from story_list;").fetchall()
        titlelist = [index[0] for index in storyinfotable]
        if len(request.form['title']) <= 40 and request.form['title'] not in titlelist:
            toadd = [request.form['title'], request.form['tag'], session['username'], request.form['firststory'],
                     request.form['firststory'], 1]
            c.execute("INSERT INTO story_list VALUES(?, ?, ?, ?, ?, ?)", toadd)
            db.commit()
            return redirect(url_for('index'))
        return render_template('create.html', error = "Title is above 40 characters or already exists")
    return render_template('create.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    storyname = request.args['storyname']
    fullstory = c.execute("SELECT fullstory from story_list WHERE storyname = '" + storyname + "';").fetchone()[0]
    contributors = c.execute("SELECT contributors from story_list WHERE storyname = '" + storyname + "';").fetchone()[0]
    totalupdates = c.execute("SELECT totalupdates from story_list WHERE storyname = '" + storyname + "';").fetchone()[0]
    if request.method == 'POST':
        newstuff = "UPDATE story_list " + "SET fullstory = '" + fullstory + " " + request.form['addition'] + "', contributors = '" + contributors + "+++" + session['username'] + "', latestupdate = '" + request.form['addition'] + "', totalupdates = " + str(totalupdates + 1) + " WHERE storyname = '" + storyname + "';"
#         c.execute("UPDATE story_list")
#         newstuff = "SET fullstory = '" + fullstory + " " + request.form['addition'] + "', contributors = '" + contributors + "+++" + session['username'] + "', latestupdate = '" + request.form['addition'] + "', totalupdates = " + str(totalupdates + 1)
        c.execute(newstuff)
#         c.execute("WHERE storyname = '" + storyname + "';")
        db.commit()
        return redirect(url_for('home'))
    return render_template('add.html', title = storyname, showuser = c.execute("SELECT latestupdate from story_list WHERE storyname = '" + storyname + "';").fetchone()[0])
    
@app.route("/story", methods=['GET', 'POST'])
def story():
    storyname = request.args['storyname']
    ver = str(c.execute("SELECT totalupdates from story_list WHERE storyname = '" + storyname + "';").fetchone()[0])
    contributors = c.execute("SELECT contributors from story_list WHERE storyname = '" + storyname + "';").fetchone()[0].split("+++")
    if session["username"] in contributors: #split contributors later
        return render_template('story.html', title = storyname, version = ver, showuser = c.execute("SELECT fullstory from story_list WHERE storyname = '" + storyname + "';").fetchone()[0])
    return render_template('story.html', title = storyname, version = ver, addmessage = "Add to this story", showuser = c.execute("SELECT latestupdate from story_list WHERE storyname = '" + storyname + "';").fetchone()[0])


@app.route("/nonfic")
def nonfic():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        if taglist[num] == "Nonfic":
            h.append(titlelist[num])
            a.append(authorlist[num])
            s.append(storylist[num])
        num += 1
    return render_template('nonfic.html', len = len(h), h = h, a = a, s = s)

@app.route("/horror")
def horror():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        if taglist[num] == "Horror":
            h.append(titlelist[num])
            a.append(authorlist[num])
            s.append(storylist[num])
        num += 1
    return render_template('horror.html', len = len(h), h = h, a = a, s = s)

@app.route("/romance")
def romance():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        if taglist[num] == "Romance":
            h.append(titlelist[num])
            a.append(authorlist[num])
            s.append(storylist[num])
        num += 1
    return render_template('romance.html', len = len(h), h = h, a = a, s = s)

@app.route("/fantasy")
def fantasy():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        if taglist[num] == "Fantasy":
            h.append(titlelist[num])
            a.append(authorlist[num])
            s.append(storylist[num])
        num += 1
    return render_template('fantasy.html', len = len(h), h = h, a = a, s = s)

@app.route("/educational")
def educational():
    storyinfotable = c.execute("SELECT * from story_list;").fetchall()
    taglist = [index[1] for index in storyinfotable]
    titlelist = [index[0] for index in storyinfotable]
    authorlist = [index[2] for index in storyinfotable]
    storylist = [index[3] for index in storyinfotable]
    h = []
    a = []
    s = []
    num = 0
    while num < len(taglist):
        if taglist[num] == "Educational":
            h.append(titlelist[num])
            a.append(authorlist[num])
            s.append(storylist[num])
        num += 1
    return render_template('educational.html', len = len(h), h = h, a = a, s = s)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
    
db.close();