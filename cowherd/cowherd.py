# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 20:30:14 2016
@author: arjun@mojolab.org
Collect information about commotion based COWMesh networks. 

"""
import sys, os, json
sys.path.append("../lib")
configfile=os.path.expanduser("~/.cowherdconfig.json")
from libcommotion import *
if __name__=="__main__":
	if len(sys.argv)<2:
		if os.popen("which cowsay").read().strip()=="/usr/games/cowsay":
			os.system("cowsay \
			'Use one of the following commands: \n \
			  gw_test_key_auth : Test key bases authentication \n \
			  show_config: Show the current manager config\n \
			  gw_get_hostname: Get and add the gateway hostname to the config\n \
			  gw_get_routes: Get and show routes from gateway\n \
			  gw_get_dhcp_leases: Get and show DhCP leases from gateway\n \
		'")
		else:
			print "Use one of the following commands: \n \
			gw_test_key_auth : Test key bases authentication \n \
			show_config: Show the current manager config\n \
			gw_get_hostname: Get and add the gateway hostname to the config\n \
			gw_get_routes: Get and show routes from host\n \
			 gw_get_dhcp_leases: Get and show DHCP leases from gateway\n \
			For some fun, install cowsay on your system"
		sys.exit()
	cowherd=CommotionCOWHerd(configfile)
	
	if sys.argv[1]=="gw_test_key_auth":
		cowherd.gw_test_key_auth()
			
	if sys.argv[1]=="show_config":
		cowherd.show_config()
	
	if sys.argv[1]=="gw_get_hostname":
		cowherd.gw_get_hostname()
			
	if sys.argv[1]=="gw_get_routes":
		cowherd.gw_get_routes()
	if sys.argv[1]=="gw_get_dhcp_leases":
		cowherd.gw_get_dhcp_leases()
	if sys.argv[1]=="gw_get_peergws":
		cowherd.gw_get_gwpeers()
	if sys.argv[1]=="runremote":
		output=cowherd.runremote(sys.argv[2],sys.argv[3],sys.argv[4])
		print output
