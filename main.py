# Developed by Seb
from flask import Flask, render_template
from post_management import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()

@app.route('/')
def index():
    return render_template("index.html")

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