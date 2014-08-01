"""
This application demonstrates the basic flow for a simple consumer of OpenID
Connect.

To authenticate the user, the application redirects to the login server, which
prompts the user for a CNetID, and redirects back, passing an authorization code
as a URL parameter. The application then exchanges the authorization code for a
longer-lived authorization token, which it then uses to read basic profile
information.

In order to run this example properly, you will need to register the application
at the production OpenID Connect server:

1. Visit https://openidcdev.uchicago.edu.
2. Click on "Self-Service Client Registration."
3. Enter "https://localhost:5000" for the Redirect URI, and click Submit.
4. Make note of the client ID and secret, and replace the values in config.py.

Next, install the Flask and requests modules. This can be done by running-

  $ pip install -r requirements.txt

-in a terminal. Finally, launch the application-

  $ python basic_client.py

-and visit http://localhost:5000 in a web browser.
"""

from flask import Flask, request, redirect, jsonify
import requests.auth, urllib
from config import CLIENT_ID, SECRET

app = Flask(__name__)

def make_url(base, **url_parameters):
    """
    Generates a UChicago-specific URI for the given request.

    Args:
        base: What endpoint, on the OpenID Connect server, to use.
        url_parameters: Key-value pair dictionary of GET parameters.

    Returns:
        The full URL for the request.
    """

    return ("https://openidcdev.uchicago.edu" + base + "?" +
            urllib.urlencode(url_parameters))

def get_token(code):
    """
    Converts a short-lived auth code into a longer-lived auth token.

    Args:
        code: The authentication code retrieved from the initial redirect.

    Returns:
        The authentication token, usable for future API requests.
    """

    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": "http://localhost:5000"}

    response = requests.post(make_url("/token"),
                             auth=client_auth,
                             data=post_data)

    token_json = response.json()
    return token_json["access_token"]

def get_user_info(access_token):
    """
    Returns basic profile information about the user.

    Args:
        access_token: The auth code returned from get_token(...).

    Returns:
        A dictionary containing a series of string keys. For example:

        {
          "email": "joe-schmo@uchicago.edu", 
          "email_verified": true, 
          "family_name": "Schmo", 
          "given_name": "Joe", 
          "middle_name": "T", 
          "name": "Joe L Schmo", 
          "preferred_username": "joe-schmo@uchicago.edu", 
          "sub": "joe-schmo@uchicago.edu"
        }
    """
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get(make_url("/userinfo"), headers=headers)
    return response.json()

@app.route("/")
def home_page():
    """
    A Flask web handler to read and output the data available in the OpenID
    Connect Userinfo endpoint.
    """

    code = request.args.get("code")
    token = request.args.get("token")

    if token:
        return jsonify(get_user_info(token))

    elif code:
        return redirect("/?" +
            urllib.urlencode(dict(token=get_token(code))))

    else:
        return redirect(make_url("/authorize",
           response_type = "code",
           client_id = CLIENT_ID,
           redirect_uri = "http://localhost:5000"))

if __name__ == "__main__":
    app.run(debug=True)