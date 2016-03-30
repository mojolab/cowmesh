import json,os,sys
from utils import *
from interfaces import *
class State:
	def __init__(self):
		self.content={}
	
	#Show own content
	def show_content(self):
		return self.content
	
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
		
	def write_state_file(self):
		f=open(self.config['system']['state_file'],"w")
		f.write(json.dumps(self.content))
		f.close()
	
	def touch(self,neighbour,content=""):
		neighbours_dir=self.config["system"]["neighbours_dir"]
		os.system("touch %s" %os.path.join(neighbours_dir,neighbour))
		if content!="":
			f=open(os.path.join(neighbours_dir,neighbour),"w")
			f.write(content)
			f.close()
	
	def get_contexts(self):		
		return self.config["contexts"]			
	
	def get_defaults(self):		
		return self.config["defaults"]
	
	def get_neighbours(self):
		neighbours=os.listdir(self.config["system"]["neighbours_dir"])
		return neighbours
		
	def get_peers(self):		
		peers=os.listdir(self.config["system"]["peers_dir"])
		return peers
	def get_interfaces(self):
		interfaces=get_hw_interfaces()
		return interfaces
	
	#Update self 
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
		

	


