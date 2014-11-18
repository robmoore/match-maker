#!/usr/bin/env python

from requests_oauthlib import OAuth2Session
from time import time

# Create a secrets.py file in same directory with client_id and client_secret defined like
# client_id = "<my_client_id>"
# client_secret = "<my_secret_id>"
# token = {
#  'access_token': '<my_access_token>'
#  'refresh_token': '<my_refresh_token>'
# }
from secrets import client_id, client_secret, token

# Uncomment for detailed oauthlib logs. Note: It doesn't appear to work. Perhaps there's a switch that's needed as weLl?
import logging
import sys
log = logging.getLogger('oauthlib')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

# Not sure it's legitimate to put the grant_token parameter here but it's unique to refresh requests and
# so doesn't make sense to put it in extra for every request.
refresh_url = "https://www.hackerschool.com/oauth/token?grant_type=refresh_token"

def issue_request(url):
  def token_updater(new_token):
      token['refresh_token'] = new_token

  # Attempting to force refresh in every instance. We could store now() + 7200 whenever we get a new access token
  # and use this value to express the expiration but we'd need to store it somewhere.
  token['expires_at'] = time() - 10

  extra = {
    'client_id': client_id,
    'client_secret': client_secret,
    # Maybe this should go here instead of in URL (see refresh_url comment above).
    #'grant_type': 'refresh_token'
  }

  hs = OAuth2Session(client_id,
                     token=token,
                     auto_refresh_kwargs=extra,
                     auto_refresh_url=refresh_url,
                     token_updater=token_updater)

  # Trigger the automatic refresh /oauth/token
  return hs.get(url)

if __name__ == '__main__':
  response = issue_request('https://www.hackerschool.com/api/v1/people/me')
  print response.json()
