#!/usr/bin/env python3

import subprocess
import re
import ipaddress
import requests
import urllib
import os

# Change this to match the desired IP range
desired_network = ipaddress.ip_network('10.0.0.0/24')


# Returns list of strings representing all local IPs this system has.
def get_local_ips():
    ifconfig_output = subprocess.run("ifconfig", capture_output=True).stdout.decode('ascii')
    # looking for "inet 111.222.33.44"-formatted matches.
    # These are ipv4 addresses, and the "inet" at the beginning means
    # it's the actual IP and not a subnet or gateway.
    inet_regex = re.compile(r'inet ([0-9\.]*)')
    return inet_regex.findall(ifconfig_output)


def get_first_local_ip_in_network(ip_list, network):
    for ip in ip_list:
        ip_obj = ipaddress.IPv4Address(ip)
        if ip_obj in network:
            return ip
    return None

ip = get_first_local_ip_in_network(get_local_ips(), desired_network)

if ip is None:
    print("No matching IPs.")
#    exit()

#print("Found IP matching the desired network: " + ip)

token = os.environ['GITHUB_TOKEN']
user = os.environ['GITHUB_USER']

endpoint_url = "https://api.github.com"
get_hooks = "/repos/{owner}/{repo}/hooks".format(owner=os.environ['GITHUB_OWNER'], repo=os.environ['GITHUB_REPO'])


def get_github_hook_target():
    response = requests.get(endpoint_url + get_hooks, auth=(user, token))
    print(response)
    print(response.json())
    ipish = re.compile(r'([0-9]*\.){3}[0-9]*')
    for hook in response.json():
        host = urllib.parse.urlparse(hook["config"]["url"])
        print(host)
        host = host.netloc
        # if host doesn't look like an IP, skip it
        # (think blah.slack.com)
        if not ipish.match(host):
            print("host {host} doesn't look like an IP".format(host=host))
            continue
        print("host {host} looks like an IP".format(host=host))
        if ipaddress.IPv4Address(host) in desired_network:
            print("found plausible IP")
            return { "id": hook["id"], "ip": host }
    return None

#def set_github_hook_

target = get_github_hook_target()
set_required = False
if target is None:
    print("no matching webhook found")
else:
    print("webook found with URL " + repr(target))
    if target.ip == ip:
        print("matches our local IP, nothing to be done")
        exit()
    print("does not match our local IP, will need to set")
    
# if old in-network address exists, replace that one
# if no in-network address exists, create a new hook
