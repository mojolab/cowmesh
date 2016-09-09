import json,os,sys
from utils import *
from interfaces import *
class State:
	def __init__(self):
		self.content={}
	
	#Show own content
	def show_content(self):
		return self.content
	
	def get_state_for_context(self,gcontext="default"):
		self.update()
		statusfull=self.content['status']
		defaults=self.config['defaults']
		contextstate={}
		for iface in statusfull['interfaces']:
			if iface['name']==defaults['iface']:
				contextstate['addr']=iface['addr']
		if gcontext=="default":
			gcontext=defaults['context']
		for context in statusfull['contexts']:
			if context['context_name']==gcontext:
				contextstate['display_name']=context['display_name']
				if 'uris' in context.keys():
					contextstate['uris']=[]
					for uri in context['uris']:
						contexturi={}
						contexturi['uri']=uri['uri'].replace("<ADDR>",contextstate['addr'])
						contexturi['uri_desc']=uri['uri_desc']
						contextstate['uris'].append(contexturi)
				if 'uuid' in context.keys():
					contextstate['uuid']=context['uuid']
		contextstate['status_uri']=defaults['status_uri'].replace("<ADDR>",contextstate['addr'])
		contextstate['lastneighbours']=self.get_neighbours()
		return contextstate
	#Load up a self image
	def load_config(self,configfile):
		f=open(configfile,"r")
		self.config=json.load(f)
		f.close()
	
	#Load state information from an existing file. 
	def load_state_file(self,state_file=None):
		if state_file==None:
			state_file=self.config['system']['state_file']
		f=open(status_file,"r")
		self.content=json.load(f)
		f.close()
	
	# Write current state to file	
	def write_state_file(self):
		f=open(self.config['system']['state_file'],"w")
		f.write(json.dumps(self.content))
		f.close()
	
	# Write touch file for neighbour
	def touch(self,neighbour,content=""):
		neighbours_dir=self.config["system"]["neighbours_dir"]
		os.system("touch %s" %os.path.join(neighbours_dir,neighbour))
		if content!="":
			f=open(os.path.join(neighbours_dir,neighbour),"w")
			f.write(content)
			f.close()
	
	# Return contexts
	def get_contexts(self):		
		return self.config["contexts"]			
	
	# Return defaults
	def get_defaults(self):		
		return self.config["defaults"]
	
	# Return neighbours
	def get_neighbours(self):
		neighbours=os.listdir(self.config["system"]["neighbours_dir"])
		return neighbours
		
	# Return peers
	def get_peers(self):		
		peers=os.listdir(self.config["system"]["peers_dir"])
		return peers
		
	# Return interfaces
	def get_interfaces(self):
		interfaces=get_hw_interfaces()
		return interfaces
	
	# Update self 
	def update(self):
		state={}
		interfaces=self.get_interfaces()
		state['interfaces']=interfaces
		contexts=self.get_contexts()
		state['contexts']=contexts
		defaults=self.get_defaults()
		state['defaults']=defaults
		neighbours=self.get_neighbours()
		state['neighbours']=neighbours
		peers=self.get_peers()
		state['peers']=peers
		self.content['status']=state
		

	


