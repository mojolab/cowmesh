import os,json, datetime
from netifaces import * 
from state import *
from datetime import *
class COWHerd:
	def __init__(self,configfilepath):
		self.configfilepath=configfilepath
		if os.path.isfile(os.path.expanduser(configfilepath)):
			f=open(os.path.expanduser(configfilepath),"r")
			self.config=json.loads(f.read())
		else: 
			self.config={'cowherd':{}}
	
	def create_config(self,ostype="debian"):
		if ostype=="debian":
			ts=datetime.now().strftime("%Y-%m-%d-%H%M%S")
			self.config['created']=ts
			hostname=os.popen("hostname").read().strip()
			self.config['cowherd']['hostname']=hostname
			self.save_config()
			self.config['cowherd']['netifaces']=[]
			
			ifaces = interfaces()
			for iface in ifaces:
				ifacedict={}
				ifacedict['name']=iface
				stateup=os.popen("ip link show %s | grep 'state UP'" %(iface)).read().strip()
				if stateup:
					ifacedict['up']=True
				if AF_INET in ifaddresses(iface).keys():
					ifacedict['ipaddr']=ifaddresses(iface)[AF_INET]
				self.config['cowherd']['netifaces'].append(ifacedict)
			self.save_config()
			gws=gateways()[AF_INET]
			self.config['gateways']=[]
			for gw in gws:
				gwdict={}
				gwdict['addr']=gw[0]
				gwdict['iface']=gw[1]
				gwdict['default']=gw[2]
				self.config['gateways'].append(gwdict)
			self.save_config()
	
	def save_config(self):
		ts=datetime.now().strftime("%Y-%m-%d-%H%M%S")
		self.config['updated']=ts
		f=open(os.path.expanduser(self.configfilepath),"w")
		f.write(json.dumps(self.config,sort_keys=True, indent=4))
		f.write("\n")
	
	def show_config(self):
		print json.dumps(self.config,sort_keys=True, indent=4)
		
	def runremote(self,command,host="localhost",user=os.environ.get("USER")):
		output=os.popen("ssh -oNumberOfPasswordPrompts=0 %s@%s '%s'" %(user,host,command)).read().strip()
		return output
	
	
	def test_key_auth(self,host,user):
		keyauth=self.runremote("echo hello",host,user)
		if keyauth=="hello":
			return True
		else:
			return False
	def runremotemulti(self,command,hostdict):
		for host in hostdict:
			self.runremote(command,host['ip'],host['user'])
	
