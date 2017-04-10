inlinklist=[]
outlinklist=[]
for link in inlinks:
	dictionary={}
	if link.startswith("/"):
		linkurl=urlparse.urljoin(baseurl,link)
	dictionary['url']=linkurl
	inlinklist.append(dictionary)
inlinkssheet=CSVFile()
inlinkssheet.colnames=['url']
inlinkssheet.matrix=inlinklist


for link in outlinks:
	dictionary={}
	if link.startswith("/"):
		linkurl=urlparse.urljoin(baseurl,link)
	dictionary['url']=linkurl
	outlinklist.append(dictionary)
outlinkssheet=CSVFile()
outlinkssheet.colnames=['url']
outlinkssheet.matrix=outlinklist
c=ExcelFile()
c.worksheets.append(inlinkssheet)
c.worksheets.append(outlinkssheet)
c.worksheetnames.append("Internal LInks")
c.worksheetnames.append("External LInks")

c.exportfile("/home/arjun/ETLinks.xlsx")
