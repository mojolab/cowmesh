import os,json, datetime
class COWHerd:
	def __init__(self,configfilepath):
		self.configfilepath=configfilepath
		f=open(configfilepath,"r")
		self.config=json.loads(f.read())
	def save_config(self):
		f=open(self.configfilepath,"w")
		f.write(json.dumps(self.config,sort_keys=True, indent=4))
		f.write("\n")
	def show_config(self):
		print json.dumps(self.config,sort_keys=True, indent=4)
	
	
	def runremote(self,command,host="localhost",user=os.environ.get("USER")):
		print "Trying to run command '%s' on host %s as user %s" %(command,host,user)
		output=os.popen("ssh -oNumberOfPasswordPrompts=0 %s@%s '%s'" %(user,host,command)).read().strip()
		return output
	
	def test_key_auth(self,host,user):
		print "Trying to log in with our key to host %s as user %s..." %(host,user)
		keyauth=self.runremote("echo hello",host,user)
		if keyauth=="hello":
			print "Key auth successful!"
			return True
		else:
			print "Copy the contents of ~/.ssh/id_rsa.pub, or wherever else you have your ssh public key to the appropriate authorized_keys file on the target"
			return False
	def get_hostname(self,host,user):
		print "Trying to get and add the hostname for %s to our config..." %host
		hostname=self.runremote("nslookup %s | grep %s | grep Address" %(host,host),host,user)
		if hostname:
			hostname=hostname.split(" ")[len(hostname.split(" "))-1]
			return hostname
		else:
			return False
