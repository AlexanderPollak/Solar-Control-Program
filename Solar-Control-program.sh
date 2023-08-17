#!/bin/bash
# Bash wrapper around python script - to set up environment
# D. Michalik, 2017

# clustertools
eval `/software/clustertools/setup.sh`

# for crython
declare -x PYTHONPATH="/software/clustertools/standard/RHEL_6_x86_64/lib/python2.7/site-packages:/home/sptdaq"

/usr/lib64/nagios/plugins/check_fridge.py
