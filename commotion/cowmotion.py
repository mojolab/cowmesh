# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 20:30:14 2016
@author: arjun@mojolab.org

Get local information on management system (the system where this program is installed)
"""
import sys, os, json
sys.path.append("../lib")
configfile=os.path.expanduser("~/.cowmeshconfig.json")
from libcommotion import *
if __name__=="__main__":
	if len(sys.argv)<2:
		print "Use one of the following commands: \n \
		gw_test_key_auth : Test key bases authentication \n \
		show_config: Show the current manager config\n \
		gw_get_hostname: Get and add the gateway hostname to the config\n \
		gw_get_routes: Get and show routes from host"
		sys.exit()
	mgr=CommotionManager(configfile)
	
	if sys.argv[1]=="gw_test_key_auth":
		print "Trying to log in with our key..."
		if mgr.gw_test_key_auth():
			print "Key auth successful!"
		else:
			print "Copy your the contents of ~/.ssh/id_rsa.pub, or wherever else you have your ssh public key registered with the gateway"
	
	if sys.argv[1]=="show_config":
		mgr.show_config()
	
	if sys.argv[1]=="gw_get_hostname":
		print "Trying to get and add the gateway hostname to our config..."
		if mgr.gw_get_hostname():
			print "Got hostname %s" %mgr.config['gwhostname']
			mgr.save_config()
	if sys.argv[1]=="gw_get_routes":
		print "Retreiving routes from gateway...."
		print mgr.gw_get_routes()
	if sys.argv[1]=="gw_get_dhcp_leases":
		print "Retreiving dhcp leases from gateway...."
		print mgr.gw_get_dhcp_leases()
