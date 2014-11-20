#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time

# Create a config file (see name below) in the same directory with the following format:
#
# [Client]
# client_id = <my_client_id>
# client_secret = <my_secret_id>
#
# [Token]
# access_token = <my_access_token>
# refresh_token = <my_refresh_token>
# expires_at = 0

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
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

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

def find_active_batches(): 
  # Look up batches
  batches = issue_request("/batches")
  # First two batches are active
  if len(batches) >= 2:
    active_batches = batches[0:2]
  else:
    active_batches = batches

  return active_batches

def find_user_by_email(email):
  # find active batches
  active_batches = find_active_batches()
  # request people in batches
  if active_batches:
    people = issue_request('/batches/' + repr(active_batches[0]['id']) + '/people')
    # Add second batch if there is one
    if len(active_batches) >= 1:
      people.extend(issue_request('/batches/' + repr(active_batches[1]['id']) + '/people'))
  
  # TODO: What happens if people is empty?
  return [person for person in people if person['email'] == email][0]

def issue_request(path):
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
  return hs.get("https://www.hackerschool.com/api/v1" + path).json()

if __name__ == '__main__':
  #manual_token_refresh()
  #print "Token refreshed"
  #response = issue_request('/people/me')
  response = find_active_batches()
  print response
  response = find_user_by_email('rob.moore@gmail.com')
  print response
