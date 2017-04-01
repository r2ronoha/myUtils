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


def print_menu():
	run("clear")	

	print "Please, select an option:"
	print ""
	print "\t1. Backup VenYa Live DB"
	print "\t2. Restore VenYa Live DB from existing backup"
	print "\t3. Import VEnYA Live DB intp the staging environtment"
	print "\t4. Start VenYa Staging environtment"
	print "\t5. (Re)start the VenYa staging Node.js server"
	print "\t6. (Re)start the VenYa staging web application"
	print "\t7. Backup the VenYa staging sources"
	print "\t8. Backup the VenYa live sources"
	print "\t9. Copy the staging sources to the live repository (will backup the live first)"
	print "\t10. Deploy VenYa to AWS, Docker HUB and GIT HUB"
	print "\t11. Commit the VenYa Android App sources to GIT HUB"
	print "\t0. EXIT"

## VARIABLES
validOptions = [ 0,1,2,3,4,5,6,7,8,9,10,11 ]
	

if __name__ == '__main__':
	print_menu()
	option = input("Select an option from above: ")

	while option not in validOptions:
		option = input("Option not valide. Please, select an option from above: ")

	print "Your choice: {}".format(option)
		
		
