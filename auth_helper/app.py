"""

Helper flask application to retrieve access token from Auth0.

$ flask run --reload --port 3000

"""


import os
import sys
import json
import webbrowser
import requests
from flask import Flask, redirect, request
import logging

def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        logger.error(f'Error: env var {var_name} is not set.')
        sys.exit(-1)
    
    
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Auth0 OAuth configuration
auth0_domain = get_env_var("AUTH0_DOMAIN")
audience = get_env_var("API_AUDIENCE")
client_id = get_env_var("AUTH0_CLIENT_ID") 
client_secret = get_env_var("AUTH0_CLIENT_SECRET") 

redirect_uri = 'http://localhost:3000/callback'          # must match the callback URL registered in Auth0 application
authorization_url = f'https://{auth0_domain}/authorize?audience={audience}&response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
token_url = f'https://{auth0_domain}/oauth/token'

@app.route('/')
def login():
    return redirect('/auth0_login')

@app.route('/auth0_login')
def auth0_login():
    webbrowser.open(authorization_url)
    return ''

@app.route('/callback')
def callback():
    #logger.info(request.__dict__)
    code = request.args['code']

    json_header = {'content-type': 'application/json'}
    token_payload = {
        'client_id':     client_id,
        'client_secret': client_secret,
        'redirect_uri':  redirect_uri,
        'code':          code,
        'grant_type':    'authorization_code'
    }    
    token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()
    access_token = token_info['access_token']
    logger.info(access_token)

    # not working
    #user_url = f'https://{auth0_domain}/userinfo?access_token={access_token}'
    #user_info = requests.get(user_url).json()
    #logger.info(user_info)

    return access_token

if __name__ == '__main__':
    app.run()


