import os
import json
from flask import request #, _request_ctx_stack
from functools import wraps
import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = [os.environ.get("AUTH0_ALGORITHMS")]
API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE")

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
    return True

#
#  Decode JWT
#
# TODO: update these examples
'''
JWKS example:

https://xxxxxx.us.auth0.com/.well-known/jwks.json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "n": "s6cwkaoAAknFPSwwO2GIBQD2dByhcZQDhUXWrA6kEZRjpWtDgh8y-5H5UMz1-rQCYWRizw_j0M9CphxvlbZVKaw3ca0HNSp1vuEcbY01jlWoRjh1dmgdBH912CSB9yGLrT_X7gknK9OoXXz5sPObwsTG_1lzrxCW-uqXBvtLTeE-ANSAOU5X5_WZnLYXNLbTWsqtP-txuhEUQwDmXl4SluRB4NUrgnH1Udq3QsT_bJx0fjHFfgsgVgCzhRSfNeYBe0D0bEJAc2GBjGCAw2zSVWZ6B65otnRm2MYLneU-UcPYWeSu48dsEC011VB3VbYeA2H-kRAUngchv4LAnbYkMw",
      "e": "AQAB",
      "kid": "shavGCaH0YCryOfo3M_h6",
      "x5t": "PUrqWFCvwuXXOEXQF9swNEH2dRE",
      "x5c": [
        "MIIDHTCCAgWgAwIBAgIJCjA73JacStYkMA0GCSqGSIb3DQEBCwUAMCwxKjAoBgNVBAMTIWRldi1ydmJ0Yzc3Yjh1ZHZhaWJ3LnVzLmF1dGgwLmNvbTAeFw0yMzA3MjExNjM1MzdaFw0zNzAzMjkxNjM1MzdaMCwxKjAoBgNVBAMTIWRldi1ydmJ0Yzc3Yjh1ZHZhaWJ3LnVzLmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALOnMJGqAAJJxT0sMDthiAUA9nQcoXGUA4VF1qwOpBGUY6VrQ4IfMvuR+VDM9fq0AmFkYs8P49DPQqYcb5W2VSmsN3GtBzUqdb7hHG2NNY5VqEY4dXZoHQR/ddgkgfchi60/1+4JJyvTqF18+bDzm8LExv9Zc68Qlvrqlwb7S03hPgDUgDlOV+f1mZy2FzS201rKrT/rcboRFEMA5l5eEpbkQeDVK4Jx9VHat0LE/2ycdH4xxX4LIFYAs4UUnzXmAXtA9GxCQHNhgYxggMNs0lVmegeuaLZ0ZtjGC53lPlHD2FnkruPHbBAtNdVQd1W2HgNh/pEQFJ4HIb+CwJ22JDMCAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUK07dm8UyeS/63pMaQ8HaU8M0SOIwDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQABm4/c+ffTV/fVawpRNOoIExAMyk94Ub7lgsaA/KQS29S/pNC1g7uoohZc7oFyRbdMD7MM/Ahx+QGG0+qCT/kW4siC8gO1pHgoo9fiPAcsO8AjlhdO39mpDhdIsG9fAvyPxTCJY/y49x+rulk7fn7V1//z1lpUX4zllvskrbGu7SzTezd3hXM8Lh6ECFcLHRjXTYX9M8N5C03F9lhIv+xFl4luTb0L8sn+ysIR4/9JKSES8ZT+cEwzvoI0As3uH4zxhBFsOOf/CH8OEgF9O68P61vmvj9YCe2Cw1qNimMG1x2afcl6lR8kBPMyHt4KmafqcigxXulpG6bxY0Dg4CZS"
      ],
      "alg": "RS256"
    },
    {
      "kty": "RSA",
      "use": "sig",
      "n": "qgvazYGTvKIqvqOFz4EZFwfzpAaQ9DpWQDFG3xKoLBIrynAnRrQe5lF6RfxcBz_Gr2HNaYkdKwddILDDdADYzCSW3lDX2-V86Lb5W5tfTVAJR8_VQh7f85TCRg8BTbleXWuBD3qzqKm-gUTqjse4FME9dSimv54QrCHHMXjtEm9sfBDnY7K4IUygVgzz31UMZQdZwEqLemgNlNedHJTtvQ7IjS4D6vkA--3X2wUe1ByR_JWvjzCF6c5eR0YhH8pKXjHjo3Y22qFQmIMdBXlOBKRHVmX5Opa_BYNG61SkLMuWIPZGKU4jtRCU7LeEyPOl1i-3tIM-gCTuIj6-I9dGcQ",
      "e": "AQAB",
      "kid": "ltDx27G4aeqjw4Hke-j0b",
      "x5t": "lWbX4ZurodR0smsHCYWyJt1ini8",
      "x5c": [
        "MIIDHTCCAgWgAwIBAgIJKmSLTg/Ue6WtMA0GCSqGSIb3DQEBCwUAMCwxKjAoBgNVBAMTIWRldi1ydmJ0Yzc3Yjh1ZHZhaWJ3LnVzLmF1dGgwLmNvbTAeFw0yMzA3MjExNjM1MzdaFw0zNzAzMjkxNjM1MzdaMCwxKjAoBgNVBAMTIWRldi1ydmJ0Yzc3Yjh1ZHZhaWJ3LnVzLmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKoL2s2Bk7yiKr6jhc+BGRcH86QGkPQ6VkAxRt8SqCwSK8pwJ0a0HuZRekX8XAc/xq9hzWmJHSsHXSCww3QA2Mwklt5Q19vlfOi2+VubX01QCUfP1UIe3/OUwkYPAU25Xl1rgQ96s6ipvoFE6o7HuBTBPXUopr+eEKwhxzF47RJvbHwQ52OyuCFMoFYM899VDGUHWcBKi3poDZTXnRyU7b0OyI0uA+r5APvt19sFHtQckfyVr48whenOXkdGIR/KSl4x46N2NtqhUJiDHQV5TgSkR1Zl+TqWvwWDRutUpCzLliD2RilOI7UQlOy3hMjzpdYvt7SDPoAk7iI+viPXRnECAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQU2b67DIF49yLIrRhRGuK/W/gvga0wDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQAqOzggeKC/BHn/2hNwXVQi9rQRmuXiV3Nyq2UUzPe4D3yuSnF7ON6C5i5U2XBrQkWSz37fBn1SFYUjfGdp0OSTzjZKLPVWLS1Gt48y0hdAnv+2G/dgm9Vaogu5DBqzHq6z2/hdzEOMI9okn24LupWvuTiDzufbzU+WXUlK2jg1SYeUGYbPz1Byd0BS3UUAJ6qbIoF2v9NiETBR1wVCoNFHCY/gy9vAmJEDPxnIzWAwuyk9MroQd114+E6ToP7LZRJAgEjiiYSiDbU4Gr3O2W0xIzODt5S0QrhEuQ3zFMoiQ8jP1dLk5fLPCuvrrPJrNL9FdKW7w3BiqLmye8rCy0YV"
      ],
      "alg": "RS256"
    }
  ]
}

Token example  (JWT format):

Format:   base64UrlEncode(header) + "." + base64UrlEncode(payload) + "." + signagure
Encoded:  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNoYXZHQ2FIMFlDcnlPZm8zTV9oNiJ9.eyJpc3MiOiJodHRwczovL2Rldi1ydmJ0Yzc3Yjh1ZHZhaWJ3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGJhZGQ3MjY5YWNlMDBiZjZhMTRjNGEiLCJhdWQiOiJjb2ZmZWltYWdlcyIsImlhdCI6MTY5MDAyOTUwNiwiZXhwIjoxNjkwMTE1OTA2LCJhenAiOiJURmZ6eWh4QjVlenZqNm1GZUcwQmF0Z1N4eDJlWk9uaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.Vj9I5Wb7G2DM6aQZxBZHruG-TprSEfevTYCqFAS2FlM58PcZ0NAPM3l1gW6jLaADr47uxlx2syyEV_ZK0bfvIVD1hKml2vStdE5stXYLDsxSiqjKR_W2c-RPeZHhRGT_0WpVIK3JylvVVMmHRLTCO95zRu89HJQNF1909zAXpKPO4DtRjFNgHkE_ISefrKCuPjnVXBl8GwHnl5Caz47Ygklmq6RcT6A4l0ZRgGKvygmR3umDXBH8oFX4aYVyqV5HyUgrOjhh-dPP42481uQxPOUi8ToTdGaLiPS-nsA_8P_HCxW2ziwuxMMECXlSMiYAKPb8Jd3Tp1Jdz2PqWlqPBg

Decoded:  (via JWT.io)
    Header:
    {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "shavGCaH0YCryOfo3M_h6"
    }
    Payload:
    {
        "iss": "https://xxxx.us.auth0.com/",
        "sub": "auth0|64badd7269ace00bf6a14c4a",
        "aud": "coffeimages",
        "iat": 1690029506,
        "exp": 1690115906,
        "azp": "TFfzyhxB5ezvj6mFeG0BatgSxx2eZOni",
        "scope": "",
        "permissions": [
            "delete:drinks",
            "get:drinks",
            "get:drinks-detail",
            "patch:drinks",
            "post:drinks"
        ]
    }    
'''
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
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=f'https://{AUTH0_DOMAIN}/')
        except jwt.JWTClaimsError:
            raise AuthError('incorrect claim', 401)
        except jwt.ExpiredSignatureError:
            raise AuthError('token expired', 401)
        except Exception:
            raise AuthError('could not parse token', 400)
    else:
        raise AuthError('could not find key', 400)
    return payload


#
#    @requires_auth() decorator method
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