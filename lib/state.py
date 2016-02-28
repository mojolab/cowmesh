import json,os,sys
from utils import *
class State:
	def __init__(self):
		self.content={}
	
	#Show own content
	def show_content(self):
		return prettydump(self.content)
	
	#Load up a self image
	def load_config(self,configfile):
		f=open(configfile,"r")
		self.config=json.load(f)
		f.close()
	#Load state information from an existing file. 
	def load_state_file(self,status_file=self.config['system']['state_file']):
		f=open(status_file,"r")
		self.content=json.load(f)
		f.close()
		
	def write_state_file(self):
		f=open(self.config['system']['state_file'],"w")
		f.write(json.dumps(self.content))
		f.close()
	
	def touch(neighbour,content=""):
		neighbours_dir=self.config["system"]["neighbours_dir"]
		os.system("touch %s" %os.path.join(neighbours_dir,neighbour))
		if content!="":
			f=open(os.path.join(neighbours_dir,neighbour),"w")
			f.write(content)
			f.close()
				
	#Update self 
	def update():
		interfaces=self.get_interfaces()
		status['interfaces']=interfaces
		contexts=self.get_contexts()
		status['contexts']=contexts
		defaults=self.get_defaults()
		status['defaults']=defaults
		neighbours=self.get_neighbours()
		status['neighbours']=neighbours
		peers=get_peers(configfile)
		status['peers']=peers
		self.content['status']=status
		

	


