import json,os, ConfigParser

protocols=['ip']

def get_ifaces_for_protocol(protocol):
	if protocol=="ip":
		ifaces=get_ipifaces()
	return ifaces

def get_ipifaces():
	iplinks=os.popen("ip link show | grep 'state UP'").read().strip().split("\n")
	ips=[]
	for link in iplinks:
		dictionary={}
		iface=link.split(": ")[1]
		ipaddr=os.popen("ip addr show %s | grep 'inet '" %iface).read().strip().split(" ")[1].split("/")[0]
		print iface,ipaddr
		dictionary['name']=iface
		dictionary['addr']=ipaddr
		dictionary['protocol']="ip"
		ips.append(dictionary)
	return ips

def get_interfaces():
	interfaces=[]
	for protocol in protocols:
		ifaces=get_ifaces_for_protocol(protocol)
		interfaces=interfaces+ifaces
	return interfaces

def get_attr_for_iface(iface,attr):
	interfaces=get_interfaces()
	for interface in interfaces:
		if interface['name']==iface:
			return interface[attr]
	return None

def get_attr_for_context(configfile,ctxt,attr):
	contexts=get_contexts(configfile)
	for context in contexts:
		if context['contextname']==ctxt:
			return context[attr]
	return None

def get_defaults(configfile):
	defaults={}
	if os.path.isfile(configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		defaults['iface']=config.get("defaults",'iface')
		defaults['protocol']=config.get("defaults",'protocol')
		defaults['context']=config.get("defaults","context")
		addr=get_attr_for_iface(defaults['iface'],'addr')
		display_name=get_attr_for_context(configfile,defaults['context'],'display_name')
		defaults['status_uri']=config.get("defaults","status_uri").replace("<ADDR>",addr)
		defaults['display_name']=display_name
	return defaults
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
			contextdict['contextname']=contextname
			contextlist.append(contextdict)
	return contextlist
			
def update_status(configfile):
	status={}
	interfaces=get_interfaces()
	status['interfaces']=interfaces
	contexts=get_contexts(configfile)
	status['contexts']=contexts
	defaults=get_defaults(configfile)
	status['defaults']=defaults
	f=open("status","w")
	f.write(json.dumps(status))
	f.close()

if __name__=="__main__":
	update_status("nwconfig.conf")
