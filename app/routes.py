from flask import render_template, url_for, request, redirect, session

from app import app
from app.authhelper import get_signin_url, get_token_from_code, access_token_is_valid
from app.graphapi import get_me

def get_redirect_uri():
    '''
    Return the location to pass to the MS OAuth2 framework
    '''
    return url_for('token', _external=True, _scheme='https')

@app.route('/')
def login():
    redirect_uri = get_redirect_uri()
    sign_in_url = get_signin_url(redirect_uri)
    context = {'sign_in_url': sign_in_url}
    return render_template('login.html', **context)

@app.route('/get_token')
def token():
    # receive the authorization code
    auth_code = request.args.get('code')
    if get_token_from_code(auth_code, get_redirect_uri()):
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/me')
def profile():
    if not access_token_is_valid(get_redirect_uri()):
        return redirect(url_for('login'))
    user = get_me()
    context = {'user': user}
    return render_template('home.html', **context)
