#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time

# Create a secrets.py file in same directory with client_id and client_secret defined like
# client_id = "<my_client_id>"
# client_secret = "<my_secret_id>"
# access_token = "<my_access_token>"
# refresh_token = "<my_refresh_token>"
from secrets import client_id, client_secret, access_token, refresh_token

# Uncomment for detailed oauthlib logs. Note: It doesn't appear to work. Perhaps there's a switch that's needed as weLl?
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
    'expires_in': "-7200"
}

def token_updater(new_token):
  global token
  token = new_token
  
def manual_token_refresh():

  extra = {
    'client_id': client_id,
    'client_secret': client_secret,
  }

  hs = OAuth2Session(client_id, token = token)
  token_updater(hs.refresh_token(refresh_url, **extra))

def issue_request(url):
  # Attempting to force refresh in every instance. We could store now() + 7200 whenever we get a new access token
  # and use this value to express the expiration but we'd need to store it somewhere.
  #token['expires_at'] = time() - 10

  extra = {
    'client_id': client_id,
    'client_secret': client_secret
  }

  hs = OAuth2Session(client_id, token=token, auto_refresh_kwargs=extra, auto_refresh_url=refresh_url, token_updater=token_updater)

  # Trigger the automatic refresh /oauth/token
  return hs.get(url)

if __name__ == '__main__':
  manual_token_refresh()
  print "Token refreshed"
  #response = issue_request('https://www.hackerschool.com/api/v1/people/me')
  #print response.json()
