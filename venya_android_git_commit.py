import re
import sys
import datetime
from contextlib import contextmanager
import os
import subprocess
from subprocess import Popen, PIPE
import getopt

@contextmanager
def cd(newdir):
	olddir = os.getcwd()
	os.chdir(os.path.expanduser(newdir))
	try:
		yield
	finally:
		os.chdir(olddir)

def run(cmd,*params):
	if type(cmd).__name__ != "str":
		print "Wrong type of command \"{}\"".format(cmd)
		sys.exit(2)

	command = cmd

	for param in params:
		if type(param).__name__ != "str":
			print "Wrong type of param \"{}\"".format(param)
			sys.exit(2)

		command += " " + param

	#openParams = ""
	cmdopen = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
	output, err = cmdopen.communicate()
	if re.search("git push",command) != None:
		return err
	if err != "":
		print "!!! ERROR !!!\nCommand \"Popen({}, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)\" FAILED\n[ERROR] \"{}\"".format(repr(command),err.rstrip())
		sys.exit(2)

	return output.rstrip()
		
## VARIABLE
basedir = os.path.join("/mnt","c","Users","arturo","OneDrive","VenYa","SOURCES","Android_app")
appdir = "venya-android-app"
git = "git"
gitmessage = ""
gitrepository = "https://r2ronoha:R2roLida@github.com/r2ronoha/venya_for_android.git"

## MAIN PROGRAM
if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:],"m:")
	except getopt.GetoptError:
		print "Failed to get program options"
		sys.exit(2)

	for opt,arg in opts:
		if opt == '-m':
			gitmessage = arg

	if gitmessage == "":
		now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		gitmessage = sys.argv[0] + " " + now
	#output = run("cd",basedir)
	with cd(basedir):
		output = run("pwd")
		print "{}\n".format(output) 
		
		output = run(git,"add",appdir)
		print "{}\n".format(output)
		
		output = run("git commit -m \"{}\"".format(gitmessage))
		print "{}\n".format(output)
		
		output = run(git,"push",gitrepository,"master")
		print "{}\n".format(output)
