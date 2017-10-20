import sys,os,json
sys.path.append("../lib")
from cowcrawl import *
import twitter
f=open("/opt/twitter.json","r")
s=json.load(f)
if __name__=="__main__":
	api=twitter.Api(consumer_key=s['consumer_key'],consumer_secret=s['consumer_secret'],access_token_key=s['access_token_key'],access_token_secret=s['access_token_secret'])
