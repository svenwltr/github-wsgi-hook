github-wsgi-hook
================

A service hook for GitHub with automatic script execution.

License
-------
Public Domain


Requirements
------------
* Python >= 2.6
* WSGI-Server (like Apache with mod_wsgi)
* netaddr 0.7 module (https://pypi.python.org/pypi/netaddr)
* Werkzeug module (https://pypi.python.org/pypi/Werkzeug)


Installing on Apache (example)
------------------------------
1. add `WSGIScriptAlias /service-hook /var/www/github-wsgi-hook/website.wsgi` to VirtualHost
2. create script `scripts/<owner-name>/<repo-name>`
