'''
Shinji, Jeffery, Sebastian
SoftDev
K<19> -- Login Session
<2022>-<11>-<3>
time spent: 2hrs
'''


from flask import Flask, render_template, request, session, redirect, url_for

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object


'''

'''

app.secret_key = '77ad3ef4fbaf3d0cd0db350b92373f8aef6ec1843bffbef0626398d52be358cf'

userpass = {}
userpass['LittleTimmy'] = 'password123'

@app.route("/")
def index():
    if 'username' in session:
        #go to main(response) page
        return redirect(url_for('response'))
    #go to login page
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login(): ## Maybe more methods will work in the /login root
    if request.method == 'POST':
        if request.form['username'] in userpass.keys():
            if userpass[request.form['username']] == request.form['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            return render_template('login.html', error = "Password is incorrect")
        return render_template('login.html', error = "Username does not exist")
    return render_template('login.html')

@app.route("/response", methods=['GET', 'POST'])
def response():
    return render_template( 'response.html' , username = session['username'])

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()