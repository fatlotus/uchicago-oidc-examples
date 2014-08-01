### OpenID Connect Example Code

This code contains three basic applications, all written in Python, and using
the excellent Flask microframework. They each advance the following goals:

1. The **basic application** (`basic_client.py`) verifies access and displays
   basic profile information;
2. The **authorizing application** (`authorizing_client.py`) verifies access and
   retrieves more information from a campus API; and
3. The **authorized API** (`authorizing_api.py`) verifies access and serves data
   to authorized applications.

If you're not sure where to start, begin with the first.

#### Installation

In order to run these examples, you will need to register the application at
the production OpenID Connect server:

1. Visit `https://openidcdev.uchicago.edu`.
2. Click on "Self-Service Client Registration."
3. Enter "`https://localhost:5000`" for the Redirect URI, and click Submit.
4. Make note of the client ID and secret, and replace the values in config.py.

Next, install the Flask and requests modules. This can be done by running-

```
$ pip install -r requirements.txt
```

-in a terminal. Finally, launch the application-

```
$ python basic_client.py
```

-and visit `http://localhost:5000` in a web browser.

#### License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
