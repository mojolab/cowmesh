#TODO Instantiate State object and expose it's functionality via server 
import os,sys,web,json
sys.path.append("../lib")
from utils import *
from state import *
from nwutils import *

configfile="/opt/nwconfig.json"
s=State()
s.load_config(configfile)

class editconfig:
	def GET(self):
		config=s.config
		configkeys=[]
		
		return '<form action="/submitform" method="post"><textarea name="jsonin" rows="40" cols="40">'+prettydump(config)+'</textarea>'  + '<input type="submit"></form>'
class submitform:
	def POST(self):
		postdata=web.data()
		return prettydump(postdata)

	
urls = (
    '/editconfig',"editconfig",
    '/submitform',"submitform",
   )

app = web.application(urls, globals())

if __name__=="__main__":	
	app.run()
