#TODO Create State class and include all this inside it
import json,os, ConfigParser

protocols=['ip']

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

def get_ifaces_for_protocol(protocol):
	if protocol=="ip":
		ifaces=get_ipifaces()
	return ifaces

def get_interfaces():
	interfaces=[]
	for protocol in protocols:
		ifaces=get_ifaces_for_protocol(protocol)
		interfaces=interfaces+ifaces
	return interfaces

def get_contexts(configfile):
	contextlist=[]
	if os.path.isfile(configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		contexts=config.sections()
		print contexts
		contexts.remove("defaults")
		contexts.remove("system")
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
	
def get_defaults(configfile):
	defaults={}
	if os.path.isfile(configfile):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		defaults['iface']=config.get("defaults",'iface')
		defaults['protocol']=config.get("defaults",'protocol')
		defaults['context']=config.get("defaults","context")
	return defaults

def get_neighbours(configfile):
	neighbours=[]
	config=ConfigParser.ConfigParser()
	config.read(configfile)
	neighbours_dir=config.get("system","neighbours_dir")
	neighbourfilenames=os.listdir(neighbours_dir)
	
	for neighbourfilename in neighbourfilenames:
		dictionary={}
		f=open(os.path.join(neighbours_dir,neighbourfilename),"r")
		try:
			j=json.load(f)
			filecontent=json.dumps(j)
		except:
			filecontent=f.read()
		dictionary['neighbour']=neighbourfilename
		dictionary['last_touch']=filecontent
		neighbours.append(dictionary)
	return neighbours

def get_peers(configfile):
	peers=[]
	config=ConfigParser.ConfigParser()
	config.read(configfile)
	peers_dir=config.get("system","peers_dir")
	peerfilenames=os.listdir(peers_dir)
	for peerfilename in peerfilenames:
		f=open(os.path.join(peers_dir,peerfilename),"r")
		try:
			j=json.load(f)
			peers.append(json.dumps(j))
		except:
			peers.append(f.read())
	return peers




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


def get_status_full():
	f=open("status","r")
	statusfull=json.load(f.read())
	f.close()
	return statusfull

def get_status_for_default_context(configfile,statusfull):
	status={}
	defaultcontext=statusfull['defaults']['context']
	defaultiface=statusfull['defaults']['iface']
	defaultaddr=get_attr_for_iface(defaultiface,'addr')
	defaultdisplay_name=get_attr_for_context(configfile,defaultcontext,'display_name')
	defaultstatus_uri=get_attr_for_context(configfile,defaultcontext,'status_uri')
	defaultuuid=get_attr_for_context(configfile,defaultcontext,"uuid")
	status['status_uri']=defaultstatus_uri.replace("0.0.0.0",defaultaddr)
	status['display_name']=defaultdisplay_name
	status['uuid']=defaultuuid
	status['peers']=statusfull['peers']
	status['neighbours']=[]
	for neighbour in statusfull['neighbours']:
		status['neighbours'].append(neighbour['neighbour'])
	
	return status
			
def update_status(configfile):
	status={}
	interfaces=get_interfaces()
	status['interfaces']=interfaces
	contexts=get_contexts(configfile)
	status['contexts']=contexts
	defaults=get_defaults(configfile)
	status['defaults']=defaults
	neighbours=get_neighbours(configfile)
	status['neighbours']=neighbours
	peers=get_peers(configfile)
	status['peers']=peers
	f=open("status","w")
	f.write(json.dumps(status))
	f.close()

if __name__=="__main__":
	update_status("nwconfig.conf")
