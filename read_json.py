# Test program to play with python
import sys
from sys import stdin
import re ## RexExp
import os
import json
import time
import subprocess
import myWindows
import file_conversions
import myUtils

def echolog(logfile,msg):
	write_log(logfile,msg)
	print(TIMESTAMP,msg,sep=' : ')

def write_log(logFileName,msg):
	TIMESTAMP = time.strftime('%Y%m%d%H%M')
	try:
		logFile = open(logFileName,"w")
	except ValueError:
		print ("Cannot open",logFileName,". Logging failed",sep=' ')

	logFile.write(TIMESTAMP + " : [read_json] " + msg)

if ( len(sys.argv) <= 1 ):
	print("Wrong syntax: " + sys.argv[0] + " <json_file> [log_file]")
	sys.exit(1)
	
logFileName = "/c/Users/arturo/OneDrive/NEW_LIFE/tmp/read_json.log"
jsonFileName = sys.argv[1]
if ( len(sys.argv) == 3 ):
	logFileName = sys.argv[2]

file_conversions.json_to_stdout(jsonFileName)

