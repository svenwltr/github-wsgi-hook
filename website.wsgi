#-*- coding: utf-8 -*-

import json
import os
import os.path
import subprocess
import datetime

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
LOG_FILE = j(a(dn(__file__)), "hook.log")

def log(msg, ip):
    with open(LOG_FILE, "a") as f:
        f.write("%s: %s - %s%s" % (datetime.datetime.now(),
                                 ip, msg, os.linesep))

@Request.application
def application(request):
    ip = "unknown"

    try:
        # check ip
        ip = IPAddress(request.remote_addr)
        for network in ALLOWED_HOSTS:
            if ip in IPNetwork(network):
                break
        else: # executed, if break isn't called
            log("Rejected, because client is in wrong network.", ip)
            return Response("You are not allowed to use this service hook.", status=403)


        # get data
        if "payload" not in request.form:
            log("Rejected, because client didn't send 'payload'.", ip)
            return Response("Incomplete request data.", status=400)
        data = json.loads(request.form['payload'])
        owner = data['repository']['owner']['name']
        repo = data['repository']["name"]


        # exec script
        script_name = j(SCRIPT_DIR, owner, repo)

        if not a(script_name).startswith(a(SCRIPT_DIR)):
            log("Rejected, because scripts doesn't point to script dir.", ip)
            return Response("Script not available.", status=400)

        if not os.path.exists(script_name):
            log("Rejected, because script for %s/%s doesn't exists." % (owner, repo), ip)
            return Response("Script not available.", status=404)

        exit = subprocess.call(script_name)

        log("Script %s/%s executed with exit code %d" % (owner, repo, exit), ip)
        return Response("OK")
    except Exception, e:
        log("Exception thrown: %s" % e, ip)
