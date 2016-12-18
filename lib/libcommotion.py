import os,json, datetime,sys
from libcowherd import *

class CommotionCOWHerd(COWHerd):		
	
	
	def gw_get_hostname(self):
		print "Trying to get and add the gateway hostname to our config..."
		gwhostname=self.get_hostname(self.config['gateway']['ip'],"root")
		if gwhostname:
			self.config['gateway']['hostname']=gwhostname
			print "Got hostname %s" %self.config['gateway']['hostname']
			self.save_config()
			return True
		else:
			return False
						
	
	def gw_get_routes(self):
		print "Retreiving routes from gateway...."
		gatewayroutes=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'ip route show'" %(self.config['gateway']['ip'])).read().strip().split("\n")
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
			self.config['gateway']['routes']=gwroutes
			self.save_config()
			return True
		else:
			print "No routes found"
			return False
	
	def gw_get_dhcp_leases(self):
		print "Retreiving dhcp leases from gateway...."
		gatewayleases=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'cat /var/dhcp.leases'" %(self.config['gateway']['ip'])).read().strip().split("\n")
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
			self.config['gateway']['dhcpleases']=gwdhcpleases
			self.save_config()
			return True
		else:
			print "No leases found"
			return False
	def gw_get_gwpeers(self):
		self.gw_get_routes()
		peergws=[]
		for route in self.config['gateway']['routes']:
			print route
			if 'gateway' in route.keys():
				print route['gateway']
				peergws.append(route['gateway'])
		peergws=list(set(peergws))
		self.config['gateway']['peergws']=peergws
		self.save_config()
		return True
