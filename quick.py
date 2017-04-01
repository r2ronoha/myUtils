import getopt
import os
import sys
import subprocess
from sys import stdin




if __name__ == "__main__":
	"""
	try:
		opts, args = getopt.getopt(argv,"f")
		myfile = args[0]
	except:
"""
	try:
		myfile = input("File to process")
	except:
		print "error"

	if os.path.isfile(myfile):
		num= 0
		fileOp = open(myfile,"r")
		for line in fileOp:
			print "{} : {}\n".format(num,line)
			num += 1
	else:
		print "File {} not found".format(myfile)
		
