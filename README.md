match-maker
===========

Finds HS pairing partners.

# Getting started

More so than the [HS wiki entry for the API](https://github.com/hackerschool/wiki/wiki/Hacker-School-API), I found [Laura Skelton's repo](https://github.com/lauraskelton/secrethandshake) to be very helpful as I sought to understand the requirements of the HS API OAuth2 implementation.

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

5. Make a copy of comm-api-client.cfg-template and name it comm-api-client.cfg. Provide your `client_id`, `client_secret`, `access_token`, and `refresh_token` created above. You may leave the `expires_at` value. It will be updated on the first
token refresh.