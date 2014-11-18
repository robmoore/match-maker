match-maker
===========

Finds HS pairing partners.

# Getting started

I found [Laura Skelton's repo](https://github.com/lauraskelton/secrethandshake) to be very helpful as I sought to understand the requirements of the HS API OAuth2 implementation.

1. From the [settings page](https://www.hackerschool.com/settings), add an OAuth application. See "Create an OAuth application" at the bottom of the page.

   *Tip:* Use `ietf:wg:oauth:2.0:oob` as your initial request URI.

2. Go to the listing of your new OAuth application and click on its name. An ID and secret for your application should appear. Make note of these values.

3. From your browser, request a URL similar to the following but substituting your client ID and secret from above:

		https://www.hackerschool.com/oauth/authorize?response_type=code&client_id=<my_client_id>&client_secret=<my_client_secret>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&site=https://www.hackerschool.com

   This will provide you a code that you can use in the next step.

4. Take the code from step 3 and use it to request an access token using the following URL but substituting the code from step 3 and your client ID and secret.

		curl -X POST https://www.hackerschool.com/oauth/token -d "grant_type=authorization_code&redirect_uri=urn:ietf:wg:oauth:2.0:oob&code=<code_from_step_3>&client_id=<my_client_id>&client_secret=<my_client_secret>"

   This request will return JSON containing your access token and refresh token. Use can test this by issuing:

		curl https://www.hackerschool.com/api/v1/people/me?access_token=<access_token_from_step_4>

5. Create a file named `secrets.py` in the same directory as the client. It should have this format:

		client_id = "<my_client_id>"
		client_secret = "<my_secret_id>"
		access_token = "<my_access_token>"
		refresh_token = "<my_refresh_token>"

   These values are pulled in to the client script with this line:

		from secrets import client_id, client_secret, token

