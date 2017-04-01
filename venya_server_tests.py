import sys
import json
import requests
import myUtils
from myUtils import run
import re
#import subprocess
#from subprocess import PIPE,Popen

venyaurl = "http://192.168.99.100:8888"

testAccount = {
	"username":"r2ronoha",
	"password":"LidaR2ro"
}

customerid = ""

server_requests = [
	["getAllCustomers","customers"],
	["getProvidersList","providers"],
	["getCustomerAppointments","appointments"]
]

def getDockerIP():
	dockerIP = run("docker-machine ls | grep 'Running' | grep '^[^ \t]\{1,\}[ \t]\{1,\}\*'")
	print "dockerIP : {}".format(dockerIP)
	if dockerIP == "":
		print "No active machine"
		runningMachine=run("docker-machine ls | grep 'Running' | grep -v 'Unknown' | head -1 | awk '{print $1}'")
		if runningMachine == "":
			print "No available machines. Exit"
			sys.exit(1)
		else:
			print "Activating machine {}".format(runningMachine)
			#envCmd = run("sh eval $(docker-machine env",runningMachine,")")
			envCmd = run("docker-machine env",runningMachine)
			#run(envCmd);
			for line in envCmd.splitlines():
				if not re.match("^#",line):
					var=line.replace("export ",'').replace("=.*",'')
					value=line.replace(".*=",'')
					print "{} : var {} -- value {}".format(line,var,value)
					#run(line)
			sys.exit(0)
			dockerIP = run("docker-machine ls | grep 'Running' | grep '^[^ \t]\{1,\}[ \t]\{1,\}\*'")
			if dockerIP == "":
				print "Unable to activate {}".format(runningMachine)
			else:
				print "Runinng IP: {}".format(dockerIP)

def printJsonField(field,value,padding,tag=""):
	if type(value).__name__ == "dict":
		jsonValue = value;
	elif type(value).__name__ == "str":
		try:	
			jsonValue = json.loads(str(value))
		except:
			#print "\nFIELD {} IS NOT JSON\n".format(field)
			print "{}{} : {}".format(padding,field,value)
			return
			#print "{} : {}".format(field,value)
	else:
		print "{}{} : {}".format(padding,field,value)
		return

	if padding == "":
		print "Next {} : {}".format(tag,field)
	else:
		print "{}{} :".format(padding,field)
	padding+="\t"
	for myField in jsonValue:
		printJsonField(myField,jsonValue[myField],padding)
		
		
def getCustomer(username=testAccount["username"],password=testAccount["password"]):
	url = venyaurl + "/getCustomer?action=login&username=" + username + "&password=" + password

	response = requests.get(url);
	try:
		jsonResp = json.loads(response.content)
	except:
		print "Faild to pareser response to getCustomer"
		return
	
	status = jsonResp["status"]
	if status != "SUCCESS":
		errormessage = jsonResp["errormessage"]
		print "getCustomer reqiest failed.\nError: {}".format(errormessage)
		return
	else:
		customerid = jsonResp["id"];
		sessionid = jsonResp["sessionid"]
		print "customerid: {}, username: {}, password: {}, session: {}".format(customerid,username,password,sessionid)
		return customerid

if __name__ == "__main__":
	getDockerIP()
	sys.exit(0)
	customerid = getCustomer()	

	for request in server_requests:
		print "=========================================="
		url = venyaurl + "/" + request[0]
		tag = request[1]
	
		if request[0] == "getCustomerAppointments":
			url += "?customerid=" + customerid
	
		print "Processing {} request ({})".format(tag,url)
		print "------------------------------------------"
		response = requests.get(url)
		#print "Response from server\n\"\n{}\n\"".format(response.content)
		try:
			jsonResp = json.loads(response.content)
		except:
			print "Failed to parse response"
			sys.exit(2)
	
		for field in jsonResp:
			print "{}".format(field)
	
		status = jsonResp["status"];
	
		if status == "SUCCESS":
			body = jsonResp[tag]
			for elt in body:
				printJsonField(elt,body[elt],"",tag)
				"""
				print "Next element: {}\n".format(elt)
				for field in body[elt]:
					if field == "_id":
						print "\tid : {}".format(body[elt][field])
					else:
						print "\t{} : {}".format(field, str(body[elt][field]["value"]))
				"""
		else:
			errormessage = jsonResp["errormessage"]
			print "ERROR: {}".format(errormessage)
	
		print "\n--------\nEND of {}\n\n".format(tag)
