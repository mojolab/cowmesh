# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 20:30:14 2016

@author: arjun@mojolab.org
"""
import sys, os

sys.path.append("../../lib")

from interfaces import *

if __name__=="__main__":
    hostname=os.popen("hostname").read().strip()
    print "***********************************"
    print "Hostname of this host: ",hostname
    print "***********************************"
    print "IP Interfaces on this host: "
    print "-----------------------------------"
    ipinterfaces = get_ifaces_for_protocol("ip")
    for interface in ipinterfaces:    
        print interface['name'],interface['addr']
    print "***********************************"
    gw=os.popen("ip route show | grep 'default' | cut -d ' ' -f 3").read().strip()
    print "Default Gateway: ",gw 
    print "***********************************"
