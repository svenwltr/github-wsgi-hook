#-*- coding: utf-8 -*-

import json
import os.path
import subprocess

from netaddr import IPNetwork, IPAddress

from werkzeug.wrappers import Request, Response
from werkzeug.debug import DebuggedApplication


j = os.path.join
dn = os.path.dirname
a = os.path.abspath


# IPs from GitHub network
ALLOWED_HOSTS = ("207.97.227.253/32", "50.57.128.197/32", "108.171.174.178/32",
                 "50.57.231.61/32", "204.232.175.64/27", "192.30.252.0/22")

SCRIPT_DIR = j(a(dn(__file__)), "scripts")

@Request.application
def application(request):

    # check ip
    ip = IPAddress(request.remote_addr)
    for network in ALLOWED_HOSTS:
        if ip in IPNetwork(network):
            break
    else: # executed, if break isn't called
        return Response("You are not allowed to use this service hook.", status=403)


    # get data
    if "payload" not in request.form:
        return Response("Incomplete request data.", status=400)
    data = json.loads(request.form['payload'])
    owner = data['repository']['owner']['name']
    repo = data['repository']["name"]


    # exec script
    script_name = j(SCRIPT_DIR, owner, repo)

    if not a(script_name).startswith(a(SCRIPT_DIR)):
        return Response("Script not available.", status=400)

    if not os.path.exists(script_name):
        return Response("Script not available.", status=404)
    subprocess.call(script_name)

    return Response("OK")
