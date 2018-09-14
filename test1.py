#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding: utf-8

# TODO(colin): fix these lint errors (http://pep8.readthedocs.io/en/release-1.7.x/intro.html#error-codes)
# pep8-disable:E128,E302
""" An interactive script for testing Khan Academy API Authentication. 

This is an example of how to use the /api/auth2 authentication flow.

See https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication for
documentation.
"""


import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser
import os
import sys
import ast
import csv

# You can get a CONSUMER_KEY and CONSUMER_SECRET for your app here:
# http://www.khanacademy.org/api-apps/register
CONSUMER_KEY = 'gKSbmeACag39m9dQ'
CONSUMER_SECRET = 'BPzwSubcn76rkpJ2'

CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'http://www.khanacademy.org'

DEFAULT_API_RESOURCE = '/api/v1/user'
VERIFIER = None


# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER

            params = cgi.parse_qs(self.path.split('?', 1)[1],
                keep_blank_values=False)
            VERIFIER = params['oauth_verifier'][0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('OAuth request token fetched and authorized;' +
                ' you can close this window.')

        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server
#Update students database

def formatString(content):
    content = content.replace('"',"'")
    content = content.replace("null","None")
    content = content.replace("false","False")
    content = content.replace("true","True")
    content = content.strip()
    return content

def updateStudentDataBase(_dir_):
    #Lê o arquivo
    file = open(_dir_,'r')
    content_file = file.read()
    file.close()

    list_user = []
    #Tratando a string 
    content_file = formatString(content_file)
    content_file[content_file.find('[{'):]

    if(content_file.find("Not Found") != -1):
        return False
    else:
        #Interpreta a string como um elemento no python[No caso list de dicts]
        list_user = eval(content_file)

        #Define-se as keys
        specif_key = ['nickname','email','username','user_id','kaid','profile_root']
        keys_ = list_user[3].keys()

        #Delete as keys desnecessárias
        for i in list_user:
            for k in keys_:
                if k not in specif_key:
                    del i[k]

        #Escreve os dados em um csv
        with open("students.csv", 'w') as f:
            writer = csv.DictWriter(f,fieldnames=['nickname','email','username','user_id','kaid','profile_root'],delimiter=";")
            writer.writeheader()
            for i in list_user:
                writer.writerow(i)

        f.close()
        return True

# Make an authenticated API call using the given rauth session.
def get_api_resource(session):

    print('\n')
    print('1 - Update students database')
    print('2 - Update students exercises info')
    print('\n')
    op = int(raw_input('Option:\t'))

    if(op):
        resource_url = "/api/v1/user/students"
        
        url = SERVER_URL + resource_url 
        split_url = url.split('?', 1)
        params = {}

        # Separate out the URL's parameters, if applicable.
        if len(split_url) == 2:
            url = split_url[0]
            params = cgi.parse_qs(split_url[1], keep_blank_values=False)

        start = time.time()
        response = session.get(url, params=params)
        end = time.time()

        #Escreve o resultado da chamada em um txt
        f = open("students-user.json","a")
        f.write(response.text.encode("utf-8"))
        f.close()

        progress = updateStudentDataBase(str("students-user.json"))
        if(progress):
            print('Atualização bem sucedida')
        else:
            print('Falha na atualização')
        
    elif op == 2:
        print('\nOp2\n')

    print("\nTempo de consulta a API: %ss\n" % (end - start))

def run_tests():
    global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL
    
    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.
    CONSUMER_KEY = raw_input("consumer key: ") or CONSUMER_KEY
    CONSUMER_SECRET = raw_input("consumer secret: ") or CONSUMER_SECRET
    SERVER_URL = raw_input("server base url: ") or SERVER_URL

    # Create an OAuth1Service using rauth.
    service = rauth.OAuth1Service(
           name='test',
           consumer_key=CONSUMER_KEY,
           consumer_secret=CONSUMER_SECRET,
           request_token_url=SERVER_URL + '/api/auth2/request_token',
           access_token_url=SERVER_URL + '/api/auth2/access_token',
           authorize_url=SERVER_URL + '/api/auth2/authorize',
           base_url=SERVER_URL + '/api/auth2')

    callback_server = create_callback_server()

    # 1. Get a request token.
    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': 'http://%s:%d/' %
            (CALLBACK_BASE, callback_server.server_address[1])})
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    webbrowser.open(authorize_url)

    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    while(True):
        get_api_resource(session)


def main():
    run_tests()

if __name__ == "__main__":
    main()
