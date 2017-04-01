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

if ( len(sys.argv) <= 1 ):
	print("Wrong syntax: " + sys.argv[0] + " <json_file> [log_file]")
	sys.exit(1)
	
jsonFileName = sys.argv[1]
if ( len(sys.argv) == 3 ):
	logFileName = sys.argv[2]

file_conversions.json_to_android_res(jsonFileName)

