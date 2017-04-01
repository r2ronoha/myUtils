import sys
import subprocess
from subprocess import Popen, PIPE
import os
import datetime
import getopt

## GLOBAL VARIABLES DEFINITIONS
venyahome = os.path.join("/mnt","c","Users","arturo","OneDrive","VenYa","SOURCES","DOCKER_CONTAINERS")
staginghome = os.path.join(venyahome,"STAGING")
livehome = venyahome
backupsdir = os.path.join(staginghome,"backups")

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

yes_no_options = ["y","n"]

## FIUNCTIONS DEFINITIONS
def input_choice(question,options):
	choice = raw_input(question).lower()
	while choice not in options:
		choice = input("ERR: please enter a valid option <" + str(options) + ">: ")
	return choice

def run(cmd,*params):
	if type(cmd).__name__ != "str":
		print "ERR: invalid command type"
		return False
	else:
		command = cmd

	for param in params:
		if type(param).__name__ != "str":
			print "ERR: invalid parameter type of {}".format(param)
			return False
		command = command + " " + param

	cmdopen = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = cmdopen.communicate()
	if err != "":
		print "\n** ERROR **\n\"Popen({},shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)\" Failed\nCommand error: \"{}\"\n\nEXIT".format(command,err.rstrip())
		sys.exit(2)
	return output.rstrip()

def copyfiles(files,source,dest,bkpdest,force):
	backup(files,dest,bkpdest,force)
	print ">> copy {} files from {} to {}".format(files,source,dest)
	sourcefiles = os.path.join(source,files)
	#output = run("cp","-vp",source,dest)
	output = run("cp","-vp",sourcefiles,dest)
	print "{}".format(output)

#def backup(message,source,dest):
def backup(files,source,dest,force):
	if not os.path.isdir(source):
		print "ERR: source folder {} does not exist".format(repr(source))
		return False
	elif os.path.isdir(dest) and not force:
		print "WAR: destination folder already exists"
		cont = input_choice("continue? [y/n]: ",yes_no_options)
		if cont == "n": 
			sys.exit(2)
	else: 
		print ">> creating destination folder {}".format(dest)
		output = run("mkdir","-vp",dest)
		print "{}".format(output)
	
	sourcepath = os.path.join(source,files)
	print ">> backing up {} to {}".format(sourcepath,dest)
	output = run("cp","-vp",sourcepath,dest)
	#output,err = run("cp","-vp",sourcepath,dest)
	#if ( err != "" ):
	#	print "ERR : {} ".format(err)
	#else:
	#	print "OUTPUT : {}".format(output)
	print "{}".format(output)

def main(argv):
	option = False
	try:
		opts, args = getopt.getopt(argv,"hfy",["--help","--force"])
	except getopt.GetoptError:
		print "{} [options]:\n\t-h/--help\n\t-y : answer yes to all questions\n\t-f/--force : force create/overwrite".format(sys.argv[0])
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print "{} [options]:\n\t-h/--help\n\t-y : answer yes to all questions\n\t-f/--force : force create/overwrite".format(sys.argv[0])
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
	backupdest = os.path.join(backupsdir,"live_bkp_" + timestamp)
	
	print ">> Copying web files <<"
	
	source = os.path.join(stagingweb,templatesdir)
	dest = os.path.join(liveweb,templatesdir)
	destbkp = os.path.join(backupdest,webdir,templatesdir)
	copyfiles("*.html",source,dest,destbkp,force)

	print "========================================================================"
	
	source = os.path.join(stagingweb,commondir)
	dest = os.path.join(liveweb,commondir)
	destbkp = os.path.join(backupdest,webdir,commondir)
	copyfiles("*.js",source,dest,destbkp,force)

	print "========================================================================"
	
	source = os.path.join(stagingweb,cssdir)
	dest = os.path.join(liveweb,cssdir)
	destbkp = os.path.join(backupdest,webdir,cssdir)
	copyfiles("*.css",source,dest,destbkp,force)

	print "========================================================================"
	
	source = os.path.join(stagingserver)
	dest = liveserver
	destbkp = os.path.join(backupdest,serverdir)
	copyfiles("*.js",source,dest,destbkp,force)

	print "========================================================================"
