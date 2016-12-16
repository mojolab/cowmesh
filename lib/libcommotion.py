import os,json
class CommotionCOWHerd:
	def __init__(self,configfilepath):
		self.configfilepath=configfilepath
		f=open(configfilepath,"r")
		self.config=json.loads(f.read())
		
	def gw_get_hostname(self):
		print "Trying to get and add the gateway hostname to our config..."
		gatewayhostname=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'nslookup %s | grep %s | grep Address'" %(self.config['gateway']['ip'],self.config['gateway']['ip'],self.config['gateway']['ip'])).read().strip()
		if gatewayhostname:
			gwhostname=gatewayhostname.split(" ")[len(gatewayhostname.split(" "))-1]
			self.config['gateway']['hostname']=gwhostname
			print "Got hostname %s" %self.config['gateway']['hostname']
			self.save_config()
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
		print "Trying to log in with our key..."
		keyauth=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'echo hello'" %self.config['gateway']['ip']).read().strip()
		if keyauth=="hello":
			print "Key auth successful!"
			return True
		else:
			print "Copy your the contents of ~/.ssh/id_rsa.pub, or wherever else you have your ssh public key registered with the gateway"
			return False
	def gw_get_routes(self):
		print "Retreiving routes from gateway...."
		gatewayroutes=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'ip route show'" %(self.config['gateway']['ip'])).read().strip().split("\n")
		if gatewayroutes:
			print gatewayroutes
			return True
	def gw_get_dhcp_leases(self):
		print "Retreiving dhcp leases from gateway...."
		gatewayleases=os.popen("ssh -oNumberOfPasswordPrompts=0 root@%s 'cat /var/dhcp.leases'" %(self.config['gateway']['ip'])).read().strip().split("\n")
		if gatewayleases:
			print gatewayleases	
			return True
