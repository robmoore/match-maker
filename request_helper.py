#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time
from urlparse import urlparse

import ConfigParser

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
    self.config = self.lookup_config()
    self.token = self.make_token()

  def lookup_config(self):
    config = ConfigParser.ConfigParser()
    config.read(self.config_file)

    client_id = config.get(self.hostname, 'client_id')
    client_secret = config.get(self.hostname, 'client_secret')
    access_token = config.get(self.hostname, 'access_token')
    refresh_token = config.get(self.hostname, 'refresh_token')
    expires_at = config.getint(self.hostname, 'expires_at')

    config = {
      'client_id': client_id,
      'client_secret': client_secret,
      'access_token': access_token,
      'refresh_token': refresh_token,
      'expires_at': expires_at
    }

    return config
    
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
    self.config.set(self.hostname, 'access_token', token['access_token'])
    self.config.set(self.hostname, 'refresh_token', token['refresh_token'])
    self.config.set(self.hostname, 'expires_at', int(token['expires_at']))
    with open(self.config_file, 'wb') as configfile:
      config.write(configfile)

  def issue_request(self, path):
    # Attempting to force refresh in every instance. We could store now() + 7200 whenever we get a new access token
    # and use this value to express the expiration but we'd need to store it somewhere.

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
  rh = RequestHelper("https://www.hackerschool.com/oauth/token", "https://www.hackerschool.com/api/v1")
  response = rh.issue_request('/people/me')
  print response
