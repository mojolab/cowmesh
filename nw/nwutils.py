import json,os, ConfigParser


def get_interfaces():
	iplinks=os.popen("ip link show | grep 'state UP'").read().strip().split("\n")
	ips=[]
	for link in iplinks:
		dictionary={}
		iface=link.split(": ")[1]
		ipaddr=os.popen("ip addr show %s | grep 'inet '" %iface).read().strip().split(" ")[1].split("/")[0]
		print iface,ipaddr
		dictionary['iface']=iface
		dictionary['ipaddr']=ipaddr
		ips.append(dictionary)
	return ips

def get_defaults(configfile):
	defaults={}
	if os.path.isfile(configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		defaults['iface']=config.get("defaults",'iface')
		defaults['protocol']=config.get("defaults",'protocol')
		defaults['context']=config.get("defaults","context")
	return json.dumps(defaults)
1
def get_contexts(configfile):
	contextlist=[]
	if os.path.isfile(configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		contexts=config.sections()
		print contexts
		contexts.remove("defaults")
		for context in contexts:
			dictionary={}
			contextname=context
			contextdict={}
			keys=config.options(context)
			for key in keys:
				contextdict[key]=config.get(context,key)
			dictionary['contextname']=contextname
			dictionary['contextdict']=contextdict
			contextlist.append(dictionary)
	return contextlist
			
def update_status(configfile):
	status={}
	status['hostname']=os.popen("hostname").read().strip()
	ips=get_interfaces()
	status['ips']=ips
	contexts=get_contexts(configfile)
	status['contexts']=contexts
	defaults=get_defaults(configfile)
	status['defaults']=defaults
	f=open("status","w")
	f.write(json.dumps(status))
	f.close()

if __name__=="__main__":
	update_status("nwconfig.conf")
