import os
import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import sys


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = [os.environ['ALGORITHMS']]
API_AUDIENCE = os.environ['API_AUDIENCE']


'''
AuthError Exception
A standardized way to communicate auth failure modes.
and i used some of my code when i was practicing in the course of
(identity and Access Management)
https://github.com/sultan12100/FSND/blob/master/BasicFlaskAuth
to verify and authorize
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': f'Permission {permission} not found.'
        }, 403)
    return True


def verify_decode_jwt(token):
    response = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(response.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error decoding token headers'
        }, 401)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience\
                     and issuer.'
            }, 401)
        except jwt.JWTError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'signature invalid'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # if we are unit testing then ignore verifying and checking token
            # sys.argv[0] contains the python script file name
            # that was initially run
            if sys.argv[0] == 'test_app.py':
                return f(None, *args, **kwargs)

            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
