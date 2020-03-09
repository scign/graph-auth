import requests
import uuid
import json

from flask import session

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

# Generic API Sending
def make_api_call(method, url, payload = None, parameters = None):
    '''
    Constructs an API call to the Microsoft Graph API
    including a user agent, authorization and content type.
    The access token must have already been received and stored
    in session['access_token'].

    Parameters

    method : string value for the http method, currently supports
    GET and POST, not case sensitive
    
    url : string full URL to send the request to, including scheme
    
    payload : data to be sent in the request, translated
    internally using json.dumps(payload)
    
    parameters : dict of any additional params to be sent

    Returns
    
    requests.Response object
    '''
    # Send these headers with all API calls
    headers = {
        'User-Agent': 'python_tutorial/1.0',
        'Authorization': 'Bearer {0}'.format(session['access_token']),
        'Accept': 'application/json'
    }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true'
    }
    headers.update(instrumentation)
    
    response = None
    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

    return response

def get_me():
    '''
    Return selected details from the current user's profile
    '''
    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {'$select': 'mail,displayName,jobTitle'}
    r = make_api_call(
        'GET', graph_endpoint.format('/me'),
        "", parameters = query_parameters
    )
    if r.status_code == requests.codes['ok']:
        try:
            user = r.json()
            return user
        except:
            pass
    return r
