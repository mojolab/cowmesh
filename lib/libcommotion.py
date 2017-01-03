import os,json, datetime,sys
from libcowherd import *
from termcolor import colored
class CommotionCOWHerd(COWHerd):	
	def check_commotion(self,host,user="root"):
		print colored("Checking if ","yellow"),colored(host,"cyan"),colored(" is a Commotion router","yellow")
		output=self.runremote("ls /var/run/commotiond.pid",host,user)
		if output=="/var/run/commotiond.pid":
			print colored(host,"cyan"),colored(" is a Commotion router", "yellow")
			return True
		else:
			return False
			
	def get_hostname(self,host,user="root"):
		print colored("Getting hostname for host ","yellow"),colored(host,"cyan")
		hostname=self.runremote("nslookup %s | grep %s | grep Address" %(host,host),host,user)
		if hostname:
			hostname=hostname.split(" ")[len(hostname.split(" "))-1]
			return hostname
		else:
			return host
			
	def gw_get_routes(self,host,user="root"):
		print colored("Getting routes from host ","yellow"),colored(host,"cyan")
		if not self.test_key_auth(host):
			return False
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
			print colored("No routes found","red")
			return False
	
	def gw_get_dhcp_leases(self,host,user="root"):
		print colored("Getting DHCP leases from host ","yellow"),colored(host,"cyan")
		gatewayleases=self.runremote('cat /var/dhcp.leases',host,user).split("\n")
		if gatewayleases:
			if '' in gatewayleases:
				gatewayleases.remove('')	
			gwdhcpleases=[]
			for lease in gatewayleases:
				leasedict={}
				leasedict['exipryts']=lease.split(' ')[0]
				leasedict['macid']=lease.split(' ')[1]
				leasedict['addr']=lease.split(' ')[2]
				leasedict['name']=lease.split(' ')[3]
				if len(lease.split(' '))>3:
					leasedict['clientid']=lease.split(' ')[4]
				gwdhcpleases.append(leasedict)
			return gwdhcpleases
		else:
			print colored("No leases found","red")
			return False
	
	def gw_get_active_dhcp_clients(self,host,user="root"):
		print colored("Getting active dhcp clients from host ","yellow"),colored(host,"cyan")
		leases=self.gw_get_dhcp_leases(host)
		activeclients=[]
		for lease in leases:
			if self.is_up(lease['addr']):
				activeclients.append(lease)
		return activeclients
	
	def update_gw_hostnames(self):
		print colored("Updating hostnames for all known gateways...","yellow")
		for gw in self.config['gateways']:
			gw['hostname']=self.get_hostname(gw['addr'][0])
		self.save_config()
		
	def update_gw_routes(self):
		print colored("Updating routes for all known gateways...","yellow")
		for gw in self.config['gateways']:
			gw['routes']=self.gw_get_routes(gw['addr'][0])
		self.save_config()
	
	def update_gw_clients(self):
		print colored("Updating DHCP leases for all known gateways...","yellow")
		for gw in self.config['gateways']:
			gw['leases']=self.gw_get_active_dhcp_clients(gw['addr'][0])
		self.save_config()
	
	def update_gw_commotion(self):
		print colored("Updating commotion flag for all known gateways...","yellow")
		for gw in self.config['gateways']:
			gw['commotion']=self.check_commotion(gw['addr'][0])
		self.save_config()
	
	def get_known_gwnames(self):
		gwnames=[]
		for gw in self.config['gateways']:
			if 'hostname' in gw.keys():
				gwnames.append(gw['hostname'])
		gwnames=list(set(gwnames))
		return gwnames
	
	def get_graph_nodes(self):
		nodes=[]
		for node in self.config['graph']['nodes']:
			nodes.append(node['id'])
		nodes=list(set(nodes))
		return nodes
	
	def graph_add_nodes(self):
		nodes=self.get_graph_nodes()
		if "cowherd" not in nodes:
			cowherdnode={"id":"cowherd","group":1}
			self.config['graph']['nodes'].append(cowherdnode)
		for gw in self.config['gateways']:
			if 'hostname' in gw.keys() and gw['hostname'] not in nodes:
				gwnode={"id":gw['hostname'],'group':6}
				self.config['graph']['nodes'].append(gwnode)
		for gw in self.config['gateways']:
			if 'leases' in gw.keys():
				for lease in gw['leases']:
					leasenode={'id':lease['name'],'group':4}
					if "android" in lease['name']:
						leasenode['group']=8
					if lease['name'] not in nodes:
						self.config['graph']['nodes'].append(leasenode)
	
	def graph_add_links(self):
		nodes=self.get_graph_nodes()
		if "cowherd" in nodes:
			print "COwherd in nodes"
			linkdict={}
			linkdict['source']="cowherd"
			linkdict['value']=1
			for gw in self.config['gateways']:
				if 'default' in gw.keys() and gw['default']==True:
					if 'hostname' in gw.keys():
						linkdict['target']=gw['hostname']
						if linkdict not in self.config['graph']['links']:
							self.config['graph']['links'].append(linkdict)
						
		for gw in self.config['gateways']:
			if 'hostname' in gw.keys():
				if 'routes' in gw.keys() and gw['routes']!=False:
					for route in gw['routes']:
						if 'gateway' in route.keys():
							if self.gw_lookup_hostname(route['gateway']) in nodes:
								linkdict={}
								linkdict['source']=gw['hostname']
								linkdict['value']=3
								linkdict['target']=self.gw_lookup_hostname(route['gateway'])
								if linkdict not in self.config['graph']['links']:
									self.config['graph']['links'].append(linkdict)
				if "leases" in gw.keys():
					for lease in gw['leases']:
						if 'name' in lease.keys():
							if lease['name'] in nodes:
								linkdict={}
								linkdict['source']=gw['hostname']
								linkdict['value']=1
								linkdict['target']=lease['name']
								if linkdict not in self.config['graph']['links']:
									self.config['graph']['links'].append(linkdict)
								else:
									print "Not adding"
		self.save_config()
	def gw_lookup_hostname(self,host):
		for gw in self.config['gateways']:
			if host in gw['addr']:
				return gw['hostname']
		return False		
	def build_graph(self):
		self.graph_add_nodes()
		self.graph_add_links()
	
	def get_peer_gateways(self):
		print colored("Identifying new peer gateways...","yellow")
		curgws=[]
		routegws=[]
		for gw in self.config['gateways']:
			curgws.append(gw['addr'][0])
			if 'routes' in gw.keys() and gw['routes']!=False:
				for route in gw['routes']:
					if 'gateway' in route.keys():
						routegws.append(route['gateway'])
		newgws=list(set(routegws)-set(curgws))
		skipped=[]
		gwnames=self.get_known_gwnames()	
		for newgw in newgws:
			print colored("Checking new gateway "),colored(newgw,"cyan")
			
			newgwhostname=self.get_hostname(newgw)
			if newgwhostname in gwnames:
				for gw in self.config['gateways']:
					if 'hostname' in gw.keys() and gw['hostname']==newgwhostname:
						if newgw in gw['addr']:
							print "Address is already known"
						else:
							gw['addr'].append(newgw)
							print "Added address %s to existing host %s" %(newgw,gw['hostname'])
						skipped.append(newgw)
			else:
				gwdict={}
				gwdict['addr']=[]
				gwdict['addr'].append(newgw)
				gwdict['hostname']=newgwhostname
				self.config['gateways'].append(gwdict)
				self.save_config()
			#else:
			#	print colored("Keyauth failed...not adding ","yellow"), colored(newgw,"cyan")
			#	skipped.append(newgw)
		newadded=set(newgws)-set(skipped)
		if len(list(newadded))>0:
			print colored("New routers added ","yellow"),colored(str(list(newadded)),"cyan")
			newadd=True
		else:
			print colored("No new routers added")
			newadd=False
		return newadd

	def get_client_report(self):
		print colored("Getting clients from all known gateways...","yellow")
		self.update_gw_leases()
		numclients=0
		for gw in self.config['gateways']:
			print colored("Looking for live clients on "+gw['addr'][0]+" "+gw['hostname']+": ","yellow")
			if "leases" in gw.keys():
				for lease in gw['leases']:
					if self.is_up(lease['addr']):
						numclients+=1
		print colored("Total clients: ","yellow"),colored(str(numclients),"green")
	
	
	def build_tree(self):
		newadd=True
		self.update_gw_hostnames()
		while newadd:
			self.update_gw_routes()
			self.build_graph()
			self.update_graph()
			self.update_gw_clients()
			self.update_gw_commotion()
			newadd=self.get_peer_gateways()
		self.build_graph()
		self.update_graph()
		
