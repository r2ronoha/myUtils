#!python2.7
import sys
from sys import stdin
import re ## RexExp
import os
import json
import time
import subprocess
from subprocess import PIPE,Popen

def input_choice(question,options):
    choice = input(question).lower()
    while choice not in options:
        choice = input("Please enter a valid choice " + str(options) + " : ")
    return choice

def run(cmd,*params):
	# verify that the command is a string
	if type(cmd).__name__ != "str":
		#print "Wrong type of command {}".format(cmd)
		print ("Wrong type of command " + cmd)
		sys.exit(2)

	# initialise the command string
	command = cmd

	# iterate through arguments passed. If they are strings, add them to the command string. otherwise exit
	for param in params:
		if type(param).__name__ != "str":
			print ("Wrong type of parameter " + param)
			#print "Wrong type of parameter {}".format(param)
			sys.exit(2)
		command += " " + param

	#print "[DEBUG] Command = \"{}\"".format(command)
	cmdopen = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = cmdopen.communicate()

	if err != "":
		#print "\n !!! ERROR !!! command \"{}\" FAILED with error \"{}\"".format(command,err.rstrip())
		print ("\n !!! ERROR !!! command " + command + " FAILED with error " + err.rstrip())
		sys.exit(2)

	return out.rstrip()

