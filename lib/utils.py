import json

def prettydump(content):
	return json.dumps(content,indent=4,sort_keys=True,separators=(',', ': '))
		
