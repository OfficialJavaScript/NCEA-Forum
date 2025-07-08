# Developed by Seb
from flask import Flask, render_template, request, redirect, session
import flask_login, argon2, usermanagement
from flask_login import current_user
from post_management import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
login_manager = flask_login.LoginManager(app)
password_hasher = argon2.PasswordHasher()
ROLES = ["1", "2", "3", "4", "5"]
ROLE_NAME = ["Level 1", "Level 2", "Level 3", "Past Student", "Educator"]
TOPICS = ['levelone', 'leveltwo', 'levelthree', 'caas', 'endorsement', 'exams', 'extensions', 'external', 'internal', 'nceaportal', 'plagiarism', 'schoolleavers', 'sickness', 'tipsandtricks']

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
    session['password_error'] = False
    session['already_exists'] = False
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        print("username: ", username)
        uid = usermanagement.exists(username)
        print("uid function: ", uid)
        if uid == None:
            session['password_error'] = True
            return redirect('/login')
        try:
            authentication = password_hasher.verify(usermanagement.hash(uid), request.form.get("password"))
            print('authentication', authentication)
        except argon2.exceptions.VerifyMismatchError:
            session['password_error'] = True
            return redirect('/login')
        print("passed authentication, disabling password error")
        session['password_error'] = False
        print("passed, loading user")
        user = load_user(uid)
        print("try to print user below:")
        print(user)
        flask_login.login_user(user)
        print("allegedly logged in, about to return /")
        return redirect('/')
    else:
        if current_user.is_authenticated == True:
            return redirect('/')
        if 'password_error' in session:
            if session['password_error'] == True:
                session['password_error'] = False
                return render_template("login.html", password_error=True)
        return render_template("login.html", password_error=False)
    
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        exists = usermanagement.exists(username)
        if exists:
            session['already_exists'] = True
            return redirect("/signup")
        try:
            password_hasher.verify(password_hasher.hash(request.form.get('confirm-password')), request.form.get('password'))
        except argon2.exceptions.VerifyMismatchError:
            session['password_error'] = True
            return redirect("/signup")
        print("running role check, current role: ", request.form.get("role"))
        if request.form.get("role") not in ROLES:
            return redirect("/signup")
        user_role = ROLE_NAME[ROLES.index(request.form.get("role"))]
        print("user's role: ", user_role)
        user = {
            "USERNAME": username,
            "ID": str(usermanagement.create_user_id()),
            "PASSWORD": password_hasher.hash(request.form.get("password")),
            "ROLE": user_role,
            "PROFILE": [False, ""]
        }
        usermanagement.add_to_database(user)
        return redirect('/')
    else:
        if 'already_exists' in session:
            if session['already_exists'] == True:
                session['already_exists'] = False
                session['password_error'] = False
                return render_template("signup.html", already_exists=True, password_error=True)
        if 'password_error' in session:
            if session['password_error'] == True:
                session['password_error'] = False
                return render_template("signup.html", already_exists=False, password_error=True)
        return render_template("signup.html", already_exists=False, password_error=False)

@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect('/')
    flask_login.logout_user()
    return redirect('/')

@app.route('/forum')
def forum():
    return render_template("forum_home.html", post_total=topic_total_posts())

@app.route('/forum_example')
def forum_example():
    return render_template("forum_example.html")

@app.route('/forum/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        if current_user.is_authenticated == True:
            if request.form.get("topic").lower() not in TOPICS:
                return redirect("/forum/create_post")
            post_info = {
                "title": request.form.get("title"),
                "comment": request.form.get("comment"),
                "user": [current_user.username, current_user.id, usermanagement.role(current_user.id)],
                "id": "",
                "topic": [f"{request.form.get("topic")}"]
            }
            write_post(post_info)
            return redirect('/forum')
        return redirect('/login')
    else:
        if current_user.is_authenticated == True:
            return render_template("create_post.html")
        return redirect("/login")

@app.route('/forum/topic/<topic>')
def forum_topic(topic):
    topic = topic.lower()
    if topic not in TOPICS:
        return redirect('/forum')
    print(topic)
    return render_template("forum_topic.html", topics=load_topic_posts(topic))

@app.route('/forum/<id>')
def forum_post(id):
    content = post_information("forum", id)
    comments = []
    if content[0] == "forum":
        comments = content[2]
        content = content[1]
    return render_template("forum.html", content=content, comments=comments)

app.run(host='0.0.0.0', port=80, debug=True)