import os,json
class CommotionManager:
	def __init__(self,configfilepath):
		self.configfilepath=configfilepath
		f=open(configfilepath,"r")
		self.config=json.loads(f.read())
		
	def gw_get_hostname(self):
		gatewayhostname=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'nslookup %s | grep %s | grep Address'" %(self.config['gateway'],self.config['gateway'],self.config['gateway'])).read().strip()
		if gatewayhostname:
			gwhostname=gatewayhostname.split(" ")[len(gatewayhostname.split(" "))-1]
			self.config['gwhostname']=gwhostname
			return True
			
		else:
			return False
						
	def save_config(self):
		f=open(self.configfilepath,"w")
		f.write(json.dumps(self.config,sort_keys=True, indent=4))
		f.write("\n")
		
	def show_config(self):
		print json.dumps(self.config,sort_keys=True, indent=4)

	def gw_test_key_auth(self):
		keyauth=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'echo hello'" %self.config['gateway']).read().strip()
		if keyauth=="hello":
			return True
	def gw_get_routes(self):
		gatewayroutes=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'ip route show'" %(self.config['gateway'])).read().strip().split("\n")
		return gatewayroutes
	def gw_get_dhcp_leases(self):
		gatewayleases=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'cat /var/dhcp.leases'" %(self.config['gateway'])).read().strip().split("\n")
		return gatewayleases	
