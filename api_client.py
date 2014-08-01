"""
This application demonstrates the basic flow for a consumer of both the login
service and an example campus API.

To authenticate the user, the application redirects to the login server, which
prompts the user for a CNetID, and redirects back, passing an authorization code
as a URL parameter. The application then exchanges the authorization code for a
longer-lived authorization token, which it then uses to compute the scrabble
score of the user's CNetID.

In order to run this example properly, you will need to register the application
at the production OpenID Connect server:

1. Visit https://openidcdev.uchicago.edu.
2. Click on "Self-Service Client Registration."
3. Enter "https://localhost:5000" for the Redirect URI.
4. Add "https://localhost:6000/scrabble" to the list of scopes (under "Access"),
   and click Submit.
5. Make note of the client ID and secret, and replace the values in config.py.

Next, install the Flask and requests modules. This can be done by running-

  $ pip install -r requirements.txt

-in a terminal. Finally, launch the demo API server-

  $ python api_server.py &

-and then the application-

  $ python api_client.py

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

def get_user_scrabble_score(access_token):
    """
    Uses the API to get the scrabble score of the given user.

    Args:
        access_token: The auth code returned from get_token(...).

    Returns:
        A number describing the point total of the current user's CNetID.
    """
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get("http://localhost:6000/scrabble", headers=headers)
    return response.json()["scrabble_score"]

@app.route("/")
def home_page():
    """
    A Flask web handler to use the example API to display the Scrabble score of
    the current user's CNetID.
    """

    code = request.args.get("code")
    token = request.args.get("token")

    if token:
        return "Your scrabble score is {}.".format(
          get_user_scrabble_score(token))

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