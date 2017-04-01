# Test program to play with python
import sys
from sys import stdin
import re ## RexExp
import os
import json
import time
import subprocess
'''
def dir(*params):
    command = ["dir"]
    for param in params:
        if type(param).__name__ !=  "str":
            return False
        else:
            command = command + [param]
    #command = ["dir"] + params
    output = subprocess.check_output(command,shell=True)
    return output.decode().rstrip()
'''

def run(cmd,*params):
    if type(cmd).__name__ != "str":
        print("Invalid command")
        return False
    command = [cmd]
    
    for param in params:
        if type(param).__name__ !=  "str":
            return False
        else:
            command = command + [param]
            
    output = subprocess.check_output(command,shell=True)
    return output.decode().rstrip()

#output = dir("*json","/b")
#print  (output)
