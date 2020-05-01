#!/usr/bin/env bash

read -r -a local_ips <<< $(ifconfig | perl -n -e'/(([0-9]*\.[0-9]*){3})/ && print $1 . " "')

# if this is found at the beginning of a given IP, we assume that IP is the one of interest.
local_range="10.0"
github_token="0455bb4a41234054c645367bee86e2f5c89957f1"

for ip in "${local_ips[@]}"
do
    echo "ip is $ip"
    if [ ! -z "$(echo $ip | perl -n -e'/(10\.0[.0-9]*)/ && print $1')" ]; then
        echo "this ip matches"
        # update github settings to use this IP and remove others
    fi
done

