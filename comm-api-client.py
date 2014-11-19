#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time

# Create a secrets.py file in same directory with client_id and client_secret defined like
# client_id = "<my_client_id>"
# client_secret = "<my_secret_id>"
# access_token = "<my_access_token>"
# refresh_token = "<my_refresh_token>"
#from secrets import client_id, client_secret, access_token, refresh_token

import ConfigParser

config_file = 'comm-api-client.cfg'

config = ConfigParser.ConfigParser()
config.read(config_file)

client_id = config.get('Client', 'client_id')
client_secret = config.get('Client', 'client_secret')
access_token = config.get('Token', 'access_token')
refresh_token = config.get('Token', 'refresh_token')
expires_at = config.getint('Token', 'expires_at')

# Uncomment for detailed oauthlib logs. 
import logging
import sys
log = logging.getLogger('oauthlib')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

refresh_url = "https://www.hackerschool.com/oauth/token"

token = {
    'access_token': access_token,
    'refresh_token': refresh_token,
    'expires_at': expires_at
}

def token_updater(new_token):
  global token
  print "Updating token"
  token = new_token
  config.set('Token', 'access_token', token['access_token'])
  config.set('Token', 'refresh_token', token['refresh_token'])
  config.set('Token', 'expires_at', int(token['expires_at']))
  with open(config_file, 'wb') as configfile:
    config.write(configfile)
  
def issue_request(url):
  # Attempting to force refresh in every instance. We could store now() + 7200 whenever we get a new access token
  # and use this value to express the expiration but we'd need to store it somewhere.

  extra = {
    'client_id': client_id,
    'client_secret': client_secret
  }

  hs = OAuth2Session(client_id, 
    token=token, 
    auto_refresh_kwargs=extra, 
    auto_refresh_url=refresh_url, 
    token_updater=token_updater)

  # Trigger the automatic refresh /oauth/token
  return hs.get(url)

if __name__ == '__main__':
  #manual_token_refresh()
  #print "Token refreshed"
  response = issue_request('https://www.hackerschool.com/api/v1/people/me')
  print response.json()
