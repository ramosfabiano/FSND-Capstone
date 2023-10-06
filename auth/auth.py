import os
import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = [os.environ.get("ALGORITHMS")]
API_AUDIENCE = os.environ.get("API_AUDIENCE")

#
# Authentication Exception
#
class AuthError(Exception):
    def __init__(self, error_message, status_code):
        self.error_message = error_message
        self.status_code = status_code

#
# Process authentication header
#
def get_token_auth_header():    
    if not 'Authorization' in request.headers:
        raise AuthError('missing authorization header.', 401)
    auth_header = request.headers['Authorization']
    components = auth_header.split(' ')
    # bearer + token
    if len(components) != 2 or components[0].lower() != 'bearer':
        raise AuthError('auth header is malformed.', 401)
    #return the token part of the header
    return components[1]

#
#  Check if permission is included in payload
#
def check_permissions(permission, payload):
    if not 'permissions' in payload:
        raise AuthError('missing permissions.', 403)
    if not permission in payload['permissions']:
        raise AuthError('access is forbidden.', 403)

#
#  Decode JWT
#
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    # jwks contains the public keys of the issuer
    jwks = json.loads(jsonurl.read())  
    header = jwt.get_unverified_header(token) 
    rsa_key = {}
    if not 'kid' in header:
        raise AuthError('key id missing.', 401)
    for k in jwks['keys']:
        if k['kid'] == header['kid']:
            rsa_key = { 'kty': k['kty'], 'kid': k['kid'], 'use': k['use'],'n': k['n'],'e': k['e']}
            break
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, audience=API_AUDIENCE, issuer=f'https://{AUTH0_DOMAIN}/', algorithms=ALGORITHMS)
        except Exception as e:
            raise AuthError(f'error processing token: {str(e)}', 400)
    else:
        raise AuthError('could not find key', 400)
    return payload


#
# @requires_auth() decorator method
#
def requires_auth(permission='', enabled=True):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if (enabled):
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
