from flask import render_template

from app import app


@app.route('/')
def login():
    return render_template('login.html')
