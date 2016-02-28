#TODO Instantiate State object and expose it's functionality via server 
import os,sys,web,json
sys.path.append("../lib")
from utils import *
from state import *



from nwutils import *


configfile="./nwconfig.json"
s=State()
s.load_config(configfile)


class requester_info:
	def GET(self):
		requesterinfo={}
		keys=web.ctx.env.keys()
		for key in keys:
			requesterinfo[key]=str(web.ctx.env.get(key))
		#return requesterinfo
		touch(web.ctx.env.get("REMOTE_ADDR"),content=json.dumps(requesterinfo))
		return json.dumps(requesterinfo)
		


class poke:
	def GET(self):
		remoteaddr = web.ctx.env.get('REMOTE_ADDR')
		remoteurl = "http://"+remoteaddr+"/nw/status"
		touch(web.ctx.env.get("REMOTE_ADDR"))
		return remoteurl

class status_ext:
	def GET(self):
		update_status(configfile)
		statusfull=get_status_full()
		touch(web.ctx.env.get("REMOTE_ADDR"))
		return json.dumps(statusfull)


class status_default:
	def GET(self):
		update_status(configfile)
		statusfull=get_status_full()
		status=get_status_for_default_context(configfile,statusfull)
		touch(web.ctx.env.get("REMOTE_ADDR"))
		return json.dumps(status)
		#return json.dumps(status)

urls = (
    '/nw/status/default',"status_default",
    '/nw/status',"status_default",
    '/nw/status/ext',"status_ext",
    '/nw/poke',"poke",
    '/nw/rqi',"requester_info"
   )


app = web.application(urls, globals())



if __name__=="__main__":
	
	app.run()
