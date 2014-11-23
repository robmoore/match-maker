#!/usr/bin/env python

from request_helper import RequestHelper

refresh_url = "https://www.hackerschool.com/oauth/token"
base_url = "https://www.hackerschool.com/api/v1"

class HackerSchoolAPI(object):
  def __init__(self):
    self.rh = RequestHelper(refresh_url, base_url)

  def find_active_batches(self): 
    # Look up batches
    batches = self.rh.issue_request("/batches")
    # First two batches are active
    if len(batches) >= 2:
      active_batches = batches[0:2]
    else:
      active_batches = batches

    return active_batches

  def find_user_by_email(self, email):
    # find active batches
    active_batches = self.find_active_batches()
    # request people in batches
    if active_batches:
      people = self.rh.issue_request('/batches/' + repr(active_batches[0]['id']) + '/people')
      # Add second batch if there is one
      if len(active_batches) >= 1:
        people.extend(self.rh.issue_request('/batches/' + repr(active_batches[1]['id']) + '/people'))
    
    # TODO: What happens if people is empty?
    return [person for person in people if person['email'] == email][0]

  def find_me(self):
    return self.rh.issue_request("/people/me")

if __name__ == '__main__':
  hs_api = HackerSchoolAPI()
  response = hs_api.find_me()
  print response