import os,sys
sys.path.append("/opt/livingdata/lib")
from livdatcsvlib import *


infile=ExcelFile()

infile.importascsv("/home/arjun/ETDocs.xlsx")


