import os,json, datetime,sys
from libcowherd import *

class CommotionCOWHerd(COWHerd):	
	def check_commotion(self,host,user="root"):
		output=self.runremote("ls /var/run/commotiond.pid",host,user)
		if output=="/var/run/commotiond.pid":
			return True
		else:
			return False
	def get_hostname(self,host,user="root"):
		print "Trying to get and add the hostname for %s to our config..." %host
		hostname=self.runremote("nslookup %s | grep %s | grep Address" %(host,host),host,user)
		if hostname:
			hostname=hostname.split(" ")[len(hostname.split(" "))-1]
			return hostname
		else:
			return False
	def gw_get_routes(self,host,user="root"):
		print "Retreiving routes from gateway...."
		gatewayroutes=self.runremote('ip route show',host,user).split("\n")
		if gatewayroutes:
			gwroutes=[]
			for route in gatewayroutes:
				routedict={}
				routedict['destination']=route.split(' ')[0]
				if route.split(' ')[1]=="via":
					routedict['gateway']=route.split(' ')[2]
					routedict['device']=route.split(' ')[4]
				if route.split(' ')[1]=="dev":
					routedict['device']=route.split(' ')[2]
				print routedict
				gwroutes.append(routedict)
			return gwroutes
		else:
			print "No routes found"
			return False
	
	def gw_get_dhcp_leases(self,host,user="root"):
		print "Retreiving dhcp leases from gateway...."
		gatewayleases=self.runremote('cat /var/dhcp.leases',host,user).split("\n")
		if gatewayleases:
			gwdhcpleases=[]
			for lease in gatewayleases:
				leasedict={}
				leasedict['exipryts']=lease.split(' ')[0]
				leasedict['macid']=lease.split(' ')[1]
				leasedict['ipaddress']=lease.split(' ')[2]
				leasedict['name']=lease.split(' ')[3]
				if len(lease.split(' '))>3:
					leasedict['clientid']=lease.split(' ')[4]
				gwdhcpleases.append(leasedict)
			return gwdhcpleases
		else:
			print "No leases found"
			return False
	
