# Developed by Seb
from flask import Flask, render_template, request, redirect, session
from flask_login import current_user
from post_management import *
from mailer import *
import flask_login, argon2, usermanagement, os, threading

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
        uid = usermanagement.exists(username)
        if uid == None:
            uid = usermanagement.exists_email(username) 
            if uid == None:
                session['password_error'] = True
                return redirect('/login')
        try:
            password_hasher.verify(usermanagement.hash(uid), request.form.get("password"))
        except argon2.exceptions.VerifyMismatchError:
            session['password_error'] = True
            return redirect('/login')
        session['password_error'] = False
        verify_status = usermanagement.check_verification(uid)
        if verify_status == "Unconfirmed":
            session['verify_status'] = uid
            return redirect('/verify')
        verify_count = usermanagement.check_vcount(uid)
        if verify_count == "Reconfirm":
            session['verify_status'] = uid
            code = usermanagement.create_code()
            usermanagement.update_verification(uid, "Unconfirmed", code)
            domain = request.host_url
            verify_account = threading.Thread(target=verify_email, args=(usermanagement.get_email(uid), usermanagement.read_name(uid), uid, "Reverify Account", code, domain))
            verify_account.start()
            return redirect('/verify')
        usermanagement.update_vcount(uid, "add")
        user = load_user(uid)
        flask_login.login_user(user)
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
        username_check = usermanagement.username_check(username)
        if username_check:
            session['not_allowed_character'] = True
            return redirect('/signup')
        exists = usermanagement.exists(username)
        if exists:
            session['already_exists'] = True
            return redirect("/signup")
        email = request.form.get("email")
        exists = usermanagement.exists_email(email)
        if exists != "" and exists != None:
            session['already_exists'] = True
            return redirect("/signup")
        try:
            password_hasher.verify(password_hasher.hash(request.form.get('confirm-password')), request.form.get('password'))
        except argon2.exceptions.VerifyMismatchError:
            session['password_error'] = True
            return redirect("/signup")
        if request.form.get("role") not in ROLES:
            return redirect("/signup")
        user_role = ROLE_NAME[ROLES.index(request.form.get("role"))]
        user_id = str(usermanagement.create_user_id())
        code = usermanagement.create_code()
        domain = request.host_url
        
        verify_email(email, username, user_id, "New Account", code, domain)
        
        verify_account = threading.Thread(target=verify_email, args=(email, username, user_id, "New Account", code, domain))
        
        verify_account.start()
        user = {
            "EMAIL": email,
            "USERNAME": username,
            "ID": user_id,
            "PASSWORD": password_hasher.hash(request.form.get("password")),
            "ROLE": user_role,
            "PROFILE": [False, ""],
            "CONFIRM_STATUS": "Unconfirmed",
            "CONFIRM_CODE": code,
            "LOGIN_COUNT": 0
        }
        usermanagement.add_to_database(user)
        session['verify_status'] = user_id
        return redirect('/verify')
    else:
        if 'already_exists' in session:
            if session['already_exists'] == True:
                session['already_exists'] = False
                session['password_error'] = False
                return render_template("signup.html", already_exists=True, password_error=True, bad_char=False)
        if 'password_error' in session:
            if session['password_error'] == True:
                session['password_error'] = False
                return render_template("signup.html", already_exists=False, password_error=True, bad_char=False)
        if 'not_allowed_character' in session:
            if session['not_allowed_character'] == True:
                session['not_allowed_character'] = False
                return render_template("signup.html", already_exists=False, password_error=False, bad_char=True)
        return render_template("signup.html", already_exists=False, password_error=False, bad_char=False)

@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect('/')
    flask_login.logout_user()
    return redirect('/')

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method == "POST":
        if 'verify_status' not in session:
            return redirect('/login')
        if session['verify_status'] == None:
            return redirect('/login')
        code = request.form.get("code")
        if usermanagement.compare_verification(session["verify_status"], code):
            user_list = usermanagement.check_vcount(session["verify_status"])
            if user_list == "Reconfirm":
                usermanagement.update_vcount(session["verify_status"], "remove")
            usermanagement.update_verification(session["verify_status"], "Confirmed", "")
            session['verify_status'] = None
            return render_template("verify.html", confirmed=True, failed=False)
        else:
            return render_template("verify.html", confirmed=False, failed=True)
    else:
        param = request.args.get("code")
        if param == None or param == "":
            if 'verify_status' in session:
                if session['verify_status'] == None:
                    return redirect('/login')
                return render_template("verify.html", confirmed=False, failed=False)
            else:
                return redirect("/login")
        else:
            user_list = usermanagement.decode_user(param)
            if usermanagement.compare_verification(user_list[0], user_list[1]):
                if user_list[2] == "Reverify Account":
                    usermanagement.update_vcount(user_list[0], "remove")
                usermanagement.update_verification(user_list[0], "Confirmed", "")
                session['verify_status'] = None
                return render_template("verify.html", confirmed=True, failed=False)
            else:
                session['verify_status'] = user_list[0]
                return render_template("verify.html", confirmed=False, failed=True)

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
                "topic": [f"{request.form.get("topic")}"],
                "followers": []
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
    return render_template("forum_topic.html", topics=load_topic_posts(topic), topic_length=len(load_topic_posts(topic)))

@app.route('/forum/<id>')
def forum_post(id):
    content = post_information("forum", id)
    comments = []
    if content[0] == "forum":
        comments = content[2]
        content = content[1]
    return render_template("forum.html", content=content, comments=comments)

@app.route("/<post_type>/<id>/reply", methods=['POST'])
def post_reply(post_type, id):
    if current_user.is_authenticated:
        if post_type == "forum":
            if check_if_exists(id, "forum"):
                add_comment(id, "forum", {
                    "user": [current_user.username, current_user.id, usermanagement.role(current_user.id)],
                    "content": request.form.get("comment"),
                    "date": ""
                })
                email_post_follower(id, current_user.username, post_type, request.host_url)
                if request.referrer:
                    return redirect(request.referrer)
                else:
                    return redirect("/forum")
        elif post_type == "guide":
            check_if_exists(id, "guide")
        else:
            if request.referrer:
                return redirect(request.referrer)
            else:
                return redirect("/forum")
    else:
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect("/forum")

@app.route('/<post_type>/<pid>/follow', methods=['POST'])
def follow_post(post_type, pid):
    if current_user.is_authenticated:
        if check_if_exists(pid, post_type):
            
            add_post_follow(pid, post_type, current_user.username, usermanagement.get_email(current_user.id))
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)

app.run(host='0.0.0.0', port=80, debug=True)