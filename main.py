# Developed by Seb
from flask import Flask, render_template, request, redirect
import flask_login, argon2, usermanagement
from flask_login import current_user
from post_management import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
login_manager = flask_login.LoginManager(app)
password_hasher = argon2.PasswordHasher()

class User(flask_login.UserMixin):
    def __init__(self):
        self.username = None
        
@login_manager.user_loader
def load_user(user_id):
    with open("database.json", 'r+') as database:
        data = json.load(database)
        for user in data["USERS"]:
            if user["ID"] == user_id:
                user_acc = User()
                user_acc.id = user_id
                user_acc.username = user["USERNAME"] 
                return user_acc
    return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        uid = usermanagement.exists(username)
        if uid == None:
            return redirect('/login')
        try:
            authentication = password_hasher.verify(usermanagement.hash(uid), request.form.get("password"))
        except argon2.exceptions.VerifyMismatchError:
            return redirect('/login')
        user = load_user(uid)
        flask_login.login_user(user)
        return redirect('/')
    else:
        if current_user.is_authenticated == True:
            return redirect('/')
        return render_template("login.html")
    
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        exists = usermanagement.exists(username)
        if exists:
            return redirect("/signup")
        authentication = password_hasher.verify(password_hasher.hash(request.form.get('confirm-password')), request.form.get('password'))
        if not authentication:
            return redirect("/signup")
        user = {
            "USERNAME": username,
            "ID": usermanagement.create_user_id(),
            "PASSWORD": password_hasher.hash(request.form.get("password")),
            "ROLE": request.form.get("role"),
            "PROFILE": [False, ""]
        }
        usermanagement.add_to_database(user)
        return redirect('/')
    else:
        return render_template("signup.html")    

@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect('/')
    #change the error's to false here...
    flask_login.logout_user()
    return redirect('/')

@app.route('/forum')
def forum_test():
    return render_template("forum_example.html")

@app.route('/forum/<id>')
def forum(id):
    content = post_information("forum", id)
    comments = []
    if content[0] == "forum":
        comments = content[2]
        content = content[1]
    return render_template("forum.html", content=content, comments=comments)

app.run(host='0.0.0.0', port=80, debug=True)