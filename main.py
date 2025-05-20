# Developed by Seb
from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/forum')
def forum():
    return render_template("forum_example.html")

app.run(host='0.0.0.0', port=80, debug=True)