"""
This application demonstrates the work required by an IT Services team to build
an OpenID Connect API for broad campus use.

To authenticate the request, the API server makes a requsest to the API server
and ensures that the user has consented to accessing the given API. To validate
that the user can access the scope for "https://example.com/endpoint," ensure
that the key "example.com/endpoint" is present in the UserInfo object and is set
to "consented," aborting the request otherwise.

To run this example, first install the Flask and requests modules. This can be
done by running-

  $ pip install -r requirements.txt

-in a terminal. Finally, launch the demo API server-

  $ python api_server.py

-and visit http://localhost:6000/scrabble in a web browser. (You won't see much
unless you use a client, such as the one provided in api_client.py.)
"""

from flask import Flask, request, redirect, jsonify
import requests.auth, urllib, collections
from config import CLIENT_ID, SECRET

app = Flask(__name__)

LETTER_SCORES = collections.defaultdict(int)
LETTER_SCORES.update(dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4,
                          I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3,
                          Q=10,R=1, S=1, T=1, U=1, V=4, W=4, X=8,
                          Y=4, Z=10))

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

@app.route("/scrabble")
def scrabble_score():
    """
    An API handler to compute the scrabble score of the given user's CNetID.
    """

    auth_type, token = request.headers["Authorization"].split(" ")

    if auth_type.lower() != "bearer":
        abort(401)

    user_info = get_user_info(token)
    if user_info.get("localhost:6000/scrabble") != "consented":
        abort(401)

    cnetid, domain = user_info["sub"].split("@")
    scrabble_score = sum(LETTER_SCORES[x] for x in cnetid.upper())

    return jsonify({"scrabble_score": scrabble_score})

if __name__ == "__main__":
    app.run(debug=True, port=6000)