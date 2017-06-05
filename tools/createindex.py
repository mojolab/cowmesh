import os,sys

index="<html><head><title>TITLE</title></head><body>CONTENT</body> </html>"


if __name__=="__main__":
	dirname=sys.argv[1]
	f=open(os.path.join(dirname,"index.html"),"w")
	files=os.listdir(dirname)
	filesall=""
	#print files
	for filename in files:
		link="<div><a href='./"+filename+"'>"+filename+"</a><br></div>"
		if "." in filename:
			ext=filename.split(".")[len(filename.split("."))-1]
			#print ext
			if ext in ["avi","mp4","mpeg"]:
				link="<div><video controls><source src='./"+filename+"'></video></div>"
				
		print link
		filesall=filesall+"<br>"+link
	#print filesall
	print index.replace("CONTENT",filesall)
		
	
