#
# Dreamhost hack to run under virtualenv
# http://wiki.dreamhost.com/Passenger#Passenger_WSGI_and_virtualenv
#
# import sys, os
# INTERP = "/home/ashron24/ashron24.zelois.com/bin/python"
# #INTERP is present twice so that the new python interpreter knows the actual executable path
# if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)


# ...however I like this lighter-weight version from
# https://virtualenv.pypa.io/en/latest/userguide.html#usage

activate_this = '/home/ashron24/ashron24.zelois.com/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

#
# Actual script, running in virtualenv, below
#


import os
import sys, traceback
import mimetypes
import Cookie


#
# Authentication via google
# https://developers.google.com/identity/sign-in/web/backend-auth
#

from oauth2client import client, crypt
CLIENT_ID = '414511154154-ondr0m3as36psueop718lnn5jp87mqi9.apps.googleusercontent.com'

def xxx_verify_token(token):
    return client.verify_id_token(token, CLIENT_ID)

def verify_token(token):
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        # If multiple clients access the backend server:
        # if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
        #     raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        # if idinfo['hd'] != APPS_DOMAIN_NAME:
        #     raise crypt.AppIdentityError("Wrong hosted domain.")
        return idinfo
    except crypt.AppIdentityError:
        # Invalid token
        # userid = idinfo['sub']
        return None


#
# Our application
#

users = map(lambda s: s.strip(), open('users.txt').readlines())

def get_login(environ):
    try:
        C = Cookie.SimpleCookie()
        C.load(environ['HTTP_COOKIE'])
        token = C['gtoken'].value
        return verify_token(token)
    except:
        return None


def check_login(verified):
    if verified['email_verified']:
        return verified['email'] in users
    else:
        return False

# def application(environ, start_response):
#     start_response('200 OK', [('Content-type', 'text/plain')])
#     return [str(check_login(environ))]

def application(environ, start_response):
    # top-level exception handling because unhelpful 500s are too easy to get...
    try:
        if environ['PATH_INFO']:
            # we are trying to load a page inside the app
            login = get_login(environ)
            if login:
                if check_login(login):
                    # Note that environ['PATH_INFO'] starts with a slash
                    path = os.getcwd() + '/private' + environ['PATH_INFO']
                else:
                    path = os.getcwd() + '/public/unauthorized.html';
            else:
                path = os.getcwd() + '/public/index.html';
            (mimetype, encoding) = mimetypes.guess_type(path)
            start_response('200 OK', [('Content-type', mimetype)])
            return [open(path).read()]
        else:
            start_response('200 OK', [('Content-type', 'text/plain')])
            return ["Hello, world!"]
    except Exception, inst:
        start_response('500 Error', [('Content-type', 'text/plain')])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return [str(inst), "\n".join(lines)]
    except:
        start_response('500 Error', [('Content-type', 'text/plain')])
        return [str('Error!')]

