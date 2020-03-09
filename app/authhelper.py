import requests
from urllib.parse import urlencode

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
    except:
        pass
    return r.status_code == requests.codes['ok']