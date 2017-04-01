import sys
import subprocess
from subprocess import Popen, PIPE
import os
import datetime

## FUNCTIONS
def run(cmd,*params):
	# verify that the command is a string
	if type(cmd).__name__ != "str":
		print "Wrong type of command {}".format(cmd)
		sys.exit(2)

	# initialise the command string
	command = cmd

	# iterate through arguments passed. If they are strings, add them to the command string. otherwise exit
	for param in params:
		if type(param).__name__ != "str":
			print "Wrong type of parameter {}".format(param)
			sys.exit(2)
		command += " " + param

	#print "[DEBUG] Command = \"{}\"".format(command)
	cmdopen = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = cmdopen.communicate()

	if err != "":
		print "\n !!! ERROR !!! command \"{}\" FAILED with error \"{}\"".format(command,err.rstrip())
		sys.exit(2)

	return out.rstrip()

## VARIABLES
basedir = os.path.join("/mnt","c","Users","arturo","OneDrive","VenYa","SOURCES","DOCKER_CONTAINERS","STAGING").replace('\\','/')
webdir = "APP_CLIENT_AWS"
serverdir = "NODE_SERVER"

resources = ( 
	('templates',webdir,'*.html'),
	('common',os.path.join(webdir,"static"),'*.js'),
	('css',os.path.join(webdir,"static"),'*.css'),
	('NODE_SERVER',"",'*.js')
)


## MAIN PROGRAM
if __name__ == "__main__":
	# get current date + time (YYYY-mm-dd_HH:MM) for the backup folder name
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
	
	# create backup folder
	bkpdir = os.path.join(basedir,"backups","bkp_" + timestamp).replace('\\','/')
	cmdout = run("mkdir","-vp",bkpdir)
	print "{}".format(cmdout)

	# copy rresources to backup folder
	for res in resources:
		resname = res[0]
		resdir = res[1]
		resfiles = res[2]
		#print "[DEBUG]\nresname: {}\nresdir: {}\nresfiles: {}\n[END DEBUG]".format(resname,resdir,resfiles)

		sourcedir = os.path.join(basedir,resdir,resname).replace('\\','/')
		sourcefiles = os.path.join(sourcedir,resfiles).replace('\\','/')
		destdir = os.path.join(bkpdir,resdir,resname).replace('\\','/')

		#print "[DEBUG]\nsourcedir: {}\nsourcefiles: {}\ndestdir: {}\n[END DEBUG]".format(sourcedir,sourcefiles,destdir)

		if not os.path.isdir(sourcedir):
			print "Source directory \"{}\" not found. Skip".format(sourcedir)
		else:
			print "> Backing up {} to {}".format(sourcefiles,bkpdir)
			if not os.path.isdir(destdir):
				print "Creating \"{}\"".format(destdir)
				cmdout = run("mkdir","-vp",destdir)
				print "{}".format(cmdout)

			cmdout = run("cp","-vp",sourcefiles,destdir)
			#print "{}".format(cmdout)
		print "----"

