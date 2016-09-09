#TODO Instantiate State object and expose it's functionality via server 
import os,sys,web,json
sys.path.append("../lib")
from utils import *
from state import *
from nwutils import *


configfile="/opt/nwconfig.json"
s=State()
s.load_config(configfile)

class requester_info:
	def GET(self):
		requesterinfo={}
		keys=web.ctx.env.keys()
		for key in keys:
			requesterinfo[key]=str(web.ctx.env.get(key))
		#return requesterinfo
		s.touch(web.ctx.env.get("REMOTE_ADDR"),content=json.dumps(requesterinfo))
		return prettydump(requesterinfo)
		
class state_show:
	def GET(self):
		s.update()
		statusfull=s.show_content()
		s.touch(web.ctx.env.get("REMOTE_ADDR"))
		#return json.dumps(statusfull)
		return prettydump(statusfull)
		

urls = (
    '/nw/state',"state_show",
    '/nw/rqi',"requester_info"
   )

app = web.application(urls, globals())

if __name__=="__main__":	
	app.run()
