# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 20:30:14 2016
@author: arjun@mojolab.org

Get local information on management system (the system where this program is installed)
"""
import sys, os, json
sys.path.append("../lib")
configfile=os.path.expanduser("~/.cowmeshconfig.json")
			
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
    print "Creating config file at %s " %configfile
    mgrconfig={}
    mgrconfig['hostname']=hostname
    mgrconfig['ipinterfaces']=ipinterfaces
    mgrconfig['gateway']=gw
    mgrjsonconfig=json.dumps(mgrconfig,sort_keys=True, indent=4)
    try:
		f=open(configfile,"w")
		f.write(mgrjsonconfig)
		f.write("\n")
		f.close()
    except:
		print "Failed to create config"
	
