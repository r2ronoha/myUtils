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

def write_log(logFileName,msg):
    TIMESTAMP = time.strftime('%Y%m%d%H%M')
    try:
        logFile = open(logFileName,"w")
    except ValueError:
        print ("Cannot open",logFileName,". Logging failed",sep=' ')

    logFile.write(TIMESTAMP + " : " + msg)

print("Hello there. Let's play")

print("\nList of options:")
print("1. JSON to CONF","2. CONF to JSON",sep="\n")
list_options = ["1","2"]
option = myUtils.input_choice("choice: ",list_options)

if option == "1":
    json_files = myWindows.run("dir","*.json","/b")
    inputFile = input("Enter the JSON file to read (" + json_files.replace("\r\n",",") + "): ")
    outputFile = input("Enter the destination CONF file: ")
    file_conversions.json_to_conf(inputFile,outputFile)
elif option == "2":
    conf_files = myWindows.run("dir","*.conf","*.cfg","/b")
    inputFile = input("Enter the CONF file to read (" + conf_files.replace("\r\n",",") + "): ")
    outputFile = input("Enter the destination JSON file: ")
    file_conversions.conf_to_json(inputFile,outputFile)

display = myUtils.input_choice("Do you want to print the output file? [Y/N]: ",["y","n"])
if display.lower() == "y":
    fileContent = myWindows.run("type",outputFile)
    print(fileContent)

'''
if len(sys.argv) < 3:
    #print ("You are in:",subprocess.call("cd"),sep=' ')
    #print ("The files available are:")
    #subprocess.call("dir")
    p = subprocess.Popen("cd",stdout=subprocess.PIPE,shell=True)
    (output,err) = p.communicate()
    print ("output is " + type(output).__name__)    
    print ("You are in folder: " + output.decode())

    p_output = myWindows.dir("*.json","/b")
    if p_output == False:
        print("could not execut command")
    else:
        print ("Available files:\n" + p_output)
    #p_output = subprocess.check_output(["dir","*.json","/b"],shell=True)
    #print ("Available files:\n" + p_output.decode())
    
    #print("Enter the file to read:",end='')
    myJsonName = input("Enter the JSON file to read (" + p_output.rstrip().replace("\r\n",",") + "): ")
    myConfName = input("Enter the destination CONF file: ")
else:
    myJsonName = sys.argv[1]
    myConfName = sys.argv[2]

file_conversions.json_to_conf(myJsonName,myConfName)
'''

