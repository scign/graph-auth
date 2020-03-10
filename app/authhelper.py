import requests
from urllib.parse import urlencode
import time

from app import app
from flask import session

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com/' + app.config['AZURE_TENANT_ID']

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/oauth2/v2.0/token')

# The scopes required by the app
# make sure these are added to the API Permissions section in the App Registration
scopes = [
    'openid',
    'offline_access',
    'User.Read',
    'Calendars.Read',
    'Calendars.Read.Shared'
]

def get_signin_url(redirect_uri):
    '''
    Build the query parameters for the signin url

    Parameters

    redirect_uri : A redirect URI configured in your app registration

    Returns

    A link to an authorization endpoint including the client ID,
    redirect URI and requested scopes
    '''
    params = {
        'client_id': app.config['AZURE_APP_ID'],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ' '.join(str(i) for i in scopes)
    }
    signin_url = authorize_url.format(urlencode(params))
    return signin_url

def get_token_from_code(auth_code, redirect_uri):
    '''
    Exchange an authorization code for an access token

    Parameters

    auth_code : an authorization code received from Azure AD
    redirect_uri : a redirect URI configured in your app registration

    Returns:

    True if an access token was obtained, False otherwise
    '''
    post_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(str(i) for i in scopes),
        'client_id': app.config['AZURE_APP_ID'],
        'client_secret': app.config['AZURE_APP_SECRET']
    }
    r = requests.post(token_url, data=post_data)
    try:
        token = r.json()
        session['access_token'] = token['access_token']
        session['refresh_token'] = token['refresh_token']
        # subtract 5 minutes to prevent issues close to expiration time
        session['token_expires'] = int(time.time()) + token['expires_in'] - 300
    except:
        pass
    return r.status_code == requests.codes['ok']

def get_token_from_refresh_token(refresh_token, redirect_uri):
    '''
    Exchange a refresh token for an access token

    Parameters

    refresh_token : a refresh token received from Azure AD
    redirect_uri : a redirect URI configured in your app registration

    Returns:

    True if an access token was obtained, False otherwise
    '''
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(str(i) for i in scopes),
        'client_id': app.config['AZURE_APP_ID'],
        'client_secret': app.config['AZURE_APP_SECRET']
    }
    r = requests.post(token_url, data = post_data)
    try:
        token = r.json()
        session['access_token'] = token['access_token']
        session['refresh_token'] = token['refresh_token']
        # subtract 5 minutes to prevent issues close to expiration time
        session['token_expires'] = int(time.time()) + token['expires_in'] - 300
    except:
        pass
    return r.status_code == requests.codes['ok']

def access_token_is_valid(redirect_uri):
    '''
    Returns True if a valid access token is stored in the session, False otherwise

    Parameters

    redirect_uri : a redirect URI configured in your app registration
    '''
    # get the current token and its expiration time from the session
    if 'access_token' not in session.keys():
        return False
    current_token = session['access_token']
    expiration = session['token_expires']
    now = int(time.time())
    if (current_token and now < expiration):
        # if there's a current token, and it's still good
        return True
    else:
        # otherwise try refreshing it
        return get_token_from_refresh_token(session['refresh_token'], redirect_uri)
