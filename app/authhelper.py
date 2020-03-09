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
    # build the query parameters for the signin url
    params = {
        'client_id': app.config['AZURE_APP_ID'],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ' '.join(str(i) for i in scopes)
    }
    signin_url = authorize_url.format(urlencode(params))
    return signin_url
