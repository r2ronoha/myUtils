import sys
from sys import stdin
import re ## RexExp
import os
import json
import time
import subprocess
import myWindows
import myUtils

def is_json(myjson):
	#print("[DEBUG] type of",myjson,"is",type(json).__name__,sep=' ')
	#try int(myjson):
	#if type(myjson).__name__ == "int":
	#	print("[DEBUG] ",myjson,"is int",sep=' ')
	#	return False
	try:
		json_object = json.loads(str(myjson))
	except ValueError:
		#print("[DEBUG] WARNING ",myjson," IS NOT JSON",sep='"')
		return False
	#print("[DEBUG] ",myjson," IS JSON",sep='"')
	return True


def read_json_to_android_res(json_str,mykey="",section=""):
	isjson = False
	#section = ""
	insection = False

	#print("[DEBUG]",json_str,"is",type(json_str).__name__)
	if type(json_str).__name__ == "str" and is_json(json_str): # if value passes is json (string + json format) run loads to convert to python dictionary
		if re.search("^[0-9]{1,}$",json_str):
			isjson = False
		else:
			parsed_json = json.loads(json_str)
			isjson = True
	elif type(json_str).__name__ == "dict": # if value is already a dictionary, assign to the parsed variable
		parsed_json = json_str
		isjson = True
	
	#if 

	if isjson:
		if mykey != "":
			section = mykey;
			#print("[" + mykey + "]") # if the value is json we print the key as config section "[key]"
		for key in list(parsed_json.keys()):
			read_json_to_android_res(parsed_json[key],key,section) # we iterate for each key in the dictionary
	else:
		if section != "":
			print("<string name=\"" + section + "_" + mykey + "\">" + str(json_str) + "</string>") # if value is not jason, print the key=value pair, as configuration parameter
		else:
			print("<string name=\"" + mykey + "\">" + str(json_str) + "</string>") # if value is not jason, print the key=value pair, as configuration parameter

def read_json_to_stdout(json_str,mykey=""):
	isjson = False

	#print("[DEBUG]",json_str,"is",type(json_str).__name__)
	if type(json_str).__name__ == "str" and is_json(json_str): # if value passes is json (string + json format) run loads to convert to python dictionary
		if re.search("^[0-9]{1,}$",json_str):
			isjson = False
		else:
			parsed_json = json.loads(json_str)
			isjson = True
	elif type(json_str).__name__ == "dict": # if value is already a dictionary, assign to the parsed variable
		parsed_json = json_str
		isjson = True
	
	#if 

	if isjson:
		if mykey != "":
			print("[" + mykey + "]") # if the value is json we print the key as config section "[key]"
		for key in list(parsed_json.keys()):
			read_json_to_stdout(parsed_json[key],key) # we iterate for each key in the dictionary
	else:
		print(mykey + "=" + str(json_str)) # if value is not jason, print the key=value pair, as configuration parameter

def read_json_to_conf(json_str,confFile,mykey=""):
	isjson = False

	print("[DEBUG]",json_str,"is",type(json_str).__name__)
	if type(json_str).__name__ == "str" and is_json(json_str): # if value passes is json (string + json format) run loads to convert to python dictionary
		if re.search("^[0-9]{1,}$",json_str):
			isjson = False
		else:
			parsed_json = json.loads(json_str)
			isjson = True
	elif type(json_str).__name__ == "dict": # if value is already a dictionary, assign to the parsed variable
		parsed_json = json_str
		isjson = True
	
	#if 

	if isjson:
		if mykey != "":
			confFile.write ("[" + mykey + "]\n") # if the value is json we print the key as config section "[key]"
		for key in list(parsed_json.keys()):
			read_json_to_conf(parsed_json[key],confFile,key) # we iterate for each key in the dictionary
	else:
		confFile.write (mykey + "=" + str(json_str) + "\n") # if value is not jason, print the key=value pair, as configuration parameter

def read_conf_to_json(confFile,jsonFile):
	section_open = False
	first_pair = False

	jsonFile.write("{\n") # write opening bracket of the file
	for line in confFile:
		line = line.rstrip()
		print("processing line: " + line)
		if not re.search("^$",line):
			if re.search("^\[.*\]$",line): # look for new section of configuration file
				section = re.sub("^\[|\]$","",line)
				if section_open:
					jsonFile.write("\n\t},\n") # if there was a previous section open, close corresponding bracket
				jsonFile.write("\t\"" + section + "\" : {\n") # open new section bracket and write key
				section_open = True
				first_pair = True
			else:
				param = line.split("=")[0] # get the name of the parameter and its value
				value = re.sub("\"","",line.split("=")[1])
				json_line = ""
				if not first_pair:
					jsonFile.write(",\n")
					#json_line = ",\n"
				if section_open:
					jsonFile.write("\t")
				json_line = "\t\"" + param + "\" : \"" + value + "\""
				jsonFile.write(json_line)
				first_pair = False

	if section_open:
		jsonFile.write("\n\t}\n") # write closing bracket for latest section, if applicable
	jsonFile.write("}") # write closing brackets for file
 

def json_replace(matchobj):
	if matchobj.group(0) == "^{": return "------- "
	elif matchobj.group(0) == "}$": return " +++++++"
	elif matchobj.group(0) == "\s": return ''

def json_to_android_res(jsonFileName):
	if os.path.isfile(jsonFileName) == False:
		print("file",jsonFileName,"not found. Exit 1",sep=' ')
		sys.exit(1)
	jsonFile = open(jsonFileName,"r")

	jsonFile_read = jsonFile.read()
	read_json_to_android_res(jsonFile_read)

def json_to_stdout(jsonFileName):
	if os.path.isfile(jsonFileName) == False:
		print("file",jsonFileName,"not found. Exit 1",sep=' ')
		sys.exit(1)
	jsonFile = open(jsonFileName,"r")

	jsonFile_read = jsonFile.read()
	read_json_to_stdout(jsonFile_read)

def json_to_conf(jsonFileName,confFileName):
	if os.path.isfile(jsonFileName) == False:
		print("file",jsonFileName,"not found. Exit 1",sep=' ')
		sys.exit(1)
	jsonFile = open(jsonFileName,"r")

	if os.path.isfile(confFileName):
		opt = myUtils.input_choice("File " + confFileName + " already exists. Overwrite? [Y/N]: ",["y","n"])
		if opt.lower() == "n":
			print("Exit. BYE")
			sys.exit(0)
	confFile = open(confFileName,"w")
	
	jsonFile_read = jsonFile.read()
	print ("\nConverting JSON file to CONFIG file\n")
	#read_json_to_stdout(jsonFile_read)
	read_json_to_conf(jsonFile_read,confFile)

def conf_to_json(confFileName,jsonFileName):	
	if os.path.isfile(confFileName) == False:
		print("file",confFileName,"not found. Exit 1",sep=' ')
		sys.exit(1)
	confFile = open(confFileName,"r")

	if os.path.isfile(jsonFileName):
		opt = myUtils.input_choice("File " + jsonFileName + " already exists. Overwrite? [Y/N]: ",["y","n"])
		#opt = input("File " + jsonFileName + " already exists. Overwrite? [Y/N]: ")
		#while re.search("^[yn]$",opt.lower()) == False:
		#	input("Please enter Y or N: ")
		if opt.lower() == "n":
			print("Exit. BYE")
			sys.exit(0)
	jsonFile = open(jsonFileName,"w")
	
	#confFile_read = confFile.read()
	print ("\nConverting JSON file to CONFIG file\n")
	#read_conf_to_stdout(confFile_read)
	read_conf_to_json(confFile,jsonFile)
