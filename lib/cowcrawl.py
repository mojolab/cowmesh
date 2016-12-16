from bs4 import BeautifulSoup

import requests

def get_links_from_url(url,prefix=None,filtered=True):
	links=[]
	resp=requests.get(url)
	soup=BeautifulSoup(resp.content,"lxml")
	if prefix==None:
		prefix=resp.url
	for link in soup.find_all("a"):
		if link.get("href").startswith("http"):
			links.append(link.get("href"))
		else:
			if filtered==True:
				if link.get("href") not in prefix and link.get("href").startswith("?")==False:
					links.append(prefix+link.get("href"))
			else:
				links.append(prefix+link.get("href"))
	return links
