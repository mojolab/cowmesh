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
		hostname=self.runremote("nslookup %s | grep %s | grep Address" %(host,host),host,user)
		if hostname:
			hostname=hostname.split(" ")[len(hostname.split(" "))-1]
			return hostname
		else:
			return False
	def gw_get_routes(self,host,user="root"):
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
				gwroutes.append(routedict)
			return gwroutes
		else:
			print "No routes found"
			return False
	
	def gw_get_dhcp_leases(self,host,user="root"):
		gatewayleases=self.runremote('cat /var/dhcp.leases',host,user).split("\n")
		
		if gatewayleases:
			if '' in gatewayleases:
				gatewayleases.remove('')	
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
	
	def update_gw_hostnames(self):
		for gw in self.config['gateways']:
			gw['hostname']=self.get_hostname(gw['addr'])
		self.save_config()
	def update_gw_routes(self):
		for gw in self.config['gateways']:
			gw['routes']=self.gw_get_routes(gw['addr'])
		self.save_config()
	def update_gw_leases(self):
		for gw in self.config['gateways']:
			print gw['addr']
			gw['leases']=self.gw_get_dhcp_leases(gw['addr'])
		self.save_config()
	def update_gw_commotion(self):
		for gw in self.config['gateways']:
			gw['commotion']=self.check_commotion(gw['addr'])
		self.save_config()
	def get_peer_gateways(self):
		curgws=[]
		routegws=[]
		for gw in self.config['gateways']:
			curgws.append(gw['addr'])
			if 'routes' in gw.keys():
				for route in gw['routes']:
					if 'gateway' in route.keys():
						routegws.append(route['gateway'])
		newgws=list(set(routegws)-set(curgws))
		skipped=[]
		for newgw in newgws:
			print newgw
			if self.test_key_auth(newgw):
				gwdict={}
				gwdict['addr']=newgw
				self.config['gateways'].append(gwdict)
			else:
				print "Keyauth to %s failed...not adding" %newgw
				skipped.append(newgw)
		newadded=set(newgws)-set(skipped)
		if len(list(newadded))>0:
			print "New routers added ",list(newadded)
			newadd=True
		else:
			print "No new routers added"
			newadd=False
			
		self.save_config()
		return newadd
	def get_numclients(self):
		numclients=0
		for gw in self.config['gateways']:
			print gw['addr'],gw['hostname'],len(gw['leases'])
			numclients+=len(gw['leases'])
		print "Total clients:",numclients
	def build_tree(self):
		newadd=True
		while newadd:
			self.update_gw_hostnames()
			self.update_gw_leases()
			self.update_gw_routes()
			self.update_gw_commotion()
			newadd=self.get_peer_gateways()
		
