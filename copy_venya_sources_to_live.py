import sys
import subprocess
from subprocess import Popen, PIPE
import os
import datetime
import getopt

## GLOBAL VARIABLES DEFINITIONS
venyahome = os.path.join("c:\\","Users","arturo","OneDrive","VenYa","SOURCES","DOCKER_CONTAINERS")
staginghome = os.path.join(venyahome,"STAGING")
livehome = venyahome
#venyahome = "/c/Users/arturo/OneDrive/VenYa/SOURCES/DOCKER_CONTAINERS"
#staginghome = venyahome + "/STAGING"
#livehome = venyahome

webdir = "APP_CLIENT_AWS"
serverdir = "NODE_SERVER"
dbdir = "MongoDB"

templatesdir = "templates"
commondir = os.path.join("static","common")
cssdir = os.path.join("static","css")

stagingweb = os.path.join(staginghome,webdir)
stagingserver = os.path.join(staginghome,serverdir)
stagingdb = os.path.join(staginghome,dbdir)

liveweb = os.path.join(livehome,webdir)
liveserver = os.path.join(livehome,serverdir)
livedb = os.path.join(livehome,dbdir)

#stagingweb = staginghome + "/" + webdir
#stagingserver = staginghome + "/" + serverdir
#stagingdb = staginghome + "/" + dbdir
#
#liveweb = livehome + "/" + webdir
#liveserver = livehome + "/" + serverdir
#livedb = livehome + "/" + dbdir

yes_no_options = ["y","n"]

## FIUNCTIONS DEFINITIONS
def input_choice(question,options):
	choice = input(question).lower()
	while choice not in options:
		choice = input("please enter a valid option <" + str(options) + ">: ")
	return choice

def run(cmd,*params):
	if type(cmd).__name__ != "str":
		print("invalid command type")
		return False
	else:
		command = cmd

	for param in params:
		#print("DEBUG: adding",param,"to command",sep=' ')
		if type(param).__name__ != "str":
			print("invalid parameter type of ",param,sep=' ')
			return False
		command = command + " " + param

	#print("DEBUG: RUNING COMMAND \"",command,"\"",sep='')
	print("Popen(" + command + ",shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)")
	cmdopen = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = cmdopen.communicate()
	#output = subprocess.call(command,shell=True)
	return output.decode().rstrip(), err.decode().rstrip()
	#output = subprocess.check_output(command,shell=True)
	#return output.decode().rstrip()

def copyfiles(files,source,dest,bkpdest,force):
	backup(files,dest,bkpdest,force)
	#print("- copy",files,"files from",source,"to",dest,sep=' ')
	#run("cp","-vp",source,dest)

#def backup(message,source,dest):
def backup(files,source,dest,force):
	#print(message,"from",source,"to",dest,sep=' ')
	if not os.path.isdir(source):
		print("source folder",repr(source),"does not exist",sep=' ')
		return False
	elif os.path.isdir(dest) and not force:
		print("destination folder already exists")
		cont = input_choice("continue? [y/n]: ",yes_no_options)
		if cont == "n": 
			return False
	else: 
		print("creating destination folder",dest,sep=' ')
		#output = subprocess.check_output(["mkdir","-vp",dest])
		output,err = run("mkdir","-vp",dest)
		print("OUTPUT :",output)
		print("ERR :",err)
	
	sourcepath = os.path.join(source,files)
	print("backing up",sourcepath,"to",dest,sep=' ')
	#output = subprocess.check_output(["cp","-vp",sourcepath,dest])
	output,err = run("cp","-v",sourcepath,dest)
	print("OUTPUT :",output)
	print("ERR :",err)

def main(argv):
	option = False
	try:
		opts, args = getopt.getopt(argv,"hfy",["--help","--force"])
	except getopt.GetoptError:
		print(sys.argv[0]," [options]:\n\t-h/--help\n\t-y : answer yes to all questions\n\t-f/--force : force create/overwrite")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(sys.argv[0]," [options]:\n\t-h/--help\n\t-y : answer yes to all questions\n\t-f/--force : force create/overwrite")
			sys.exit()
		elif opt in ("-f","--force","-y"):
			option = True
	return option
		

	
## PROGRAM BODY
force = False

if __name__ == "__main__":
	force = main(sys.argv[1:])
	
	now = datetime.datetime.now()
	timestamp = now.strftime("%Y-%m-%d")
	backupdest = os.path.join(staginghome,"live_bkp_" + timestamp)
	#backupdest = staginghome + "/live_bkp_" + timestamp
	
	print(">> Copying web files <<")
	
	source = os.path.join(stagingweb,templatesdir)
	dest = os.path.join(liveweb,templatesdir)
	destbkp = os.path.join(backupdest,webdir,templatesdir)
	copyfiles("*.html",source,dest,destbkp,force)
	
#	source = os.path.join(stagingweb,commondir)
#	dest = os.path.join(liveweb,commondir)
#	destbkp = os.path.join(backupdest,webdir,commondir)
#	copyfiles("*.js",source,dest,destbkp,force)
#	
#	source = os.path.join(stagingweb,cssdir)
#	dest = os.path.join(liveweb,cssdir)
#	destbkp = os.path.join(backupdest,webdir,cssdir)
#	copyfiles("*.css",source,dest,destbkp,force)
#	
#	source = os.path.join(stagingserver)
#	dest = liveserver
#	destbkp = os.path.join(backupdest,serverdir)
#	copyfiles("*.js",source,dest,destbkp,force)
#	
#	
#	
