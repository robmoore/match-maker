#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time
from urlparse import urlparse

import ConfigParser
import sys
import requests

# Uncomment for detailed oauthlib logs. 
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

# Create a config file (see name below) in the same directory with the following format:
#
# [hostname]
# client_id = <my_client_id>
# client_secret = <my_secret_id>
# access_token = <my_access_token>
# refresh_token = <my_refresh_token>
# expires_at = 0

class RequestHelper(object):
    config_file = 'request_helper.cfg'

    def __init__(self, refresh_url, base_url):
        self.refresh_url = refresh_url
        self.base_url = base_url
        self.hostname = urlparse(refresh_url).hostname
        self.configParser = ConfigParser.ConfigParser()
        self.config = self.lookup_config()
        self.token = self.make_token()

    # Note: This may not be generic across providers
    # To get auth_code, issue the following in your browser (after replacing relevant values in the URL):
    # https://www.hackerschool.com/oauth/authorize?response_type=code&client_id=...&client_secret=...&redirect_uri=urn:ietf:wg:oauth:2.0:oob&site=https://www.hackerschool.com
    def set_tokens(self, auth_code):
        # Issue request with auth_code
        params = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'grant_type': 'authorization_code',
            'code': auth_code
        }
        r = requests.post(self.refresh_url, params=params)
        response = r.json()
        if r.status_code == requests.codes.ok:
            # set access_token and request_token
            # set expires at
            new_token = {
                'access_token': response['access_token'],
                'refresh_token': response['refresh_token'],
                'expires_at': time() + response['expires_in']
            }
            self.token_updater(new_token)
        else:
            r.raise_for_status()

    def lookup_config(self):
        self.configParser.read(self.config_file)

        client_id = self.configParser.get(self.hostname, 'client_id')
        client_secret = self.configParser.get(self.hostname, 'client_secret')
        access_token = self.configParser.get(self.hostname, 'access_token')
        refresh_token = self.configParser.get(self.hostname, 'refresh_token')
        expires_at = self.configParser.getint(self.hostname, 'expires_at')

        return {
            'client_id': client_id,
            'client_secret': client_secret,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_at': expires_at
        }
        
    def make_token(self):
        token = {
            'access_token': self.config['access_token'],
            'refresh_token': self.config['refresh_token'],
            'expires_at': self.config['expires_at']
        }

        return token

    def token_updater(self, new_token):
        print "Updating token"
        self.token = new_token
        self.configParser.set(self.hostname, 'access_token', new_token['access_token'])
        self.configParser.set(self.hostname, 'refresh_token', new_token['refresh_token'])
        self.configParser.set(self.hostname, 'expires_at', int(new_token['expires_at']))
        with open(self.config_file, 'wb') as configfile:
            self.configParser.write(configfile)

    def issue_request(self, path):
        extra = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret']
        }

        oa2s = OAuth2Session(self.config['client_id'], 
                             token = self.token, 
                             auto_refresh_kwargs = extra, 
                             auto_refresh_url = self.refresh_url, 
                             token_updater = self.token_updater)

        # Trigger the automatic refresh /oauth/token
        return oa2s.get(self.base_url + path).json()

if __name__ == '__main__':
    # auth_code is the first argument
    auth_code = sys.argv[1]
    rh = RequestHelper("https://www.hackerschool.com/oauth/token", "https://www.hackerschool.com/api/v1")
    response = rh.set_tokens(auth_code)
    print response
