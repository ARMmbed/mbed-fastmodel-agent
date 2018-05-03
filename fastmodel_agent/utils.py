#!/usr/bin/env python
"""
mbed SDK
Copyright (c) 2011-2018 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import io
import platform
import os
import sys
import time
import tempfile
import subprocess


_TEMP_STDOUT = tempfile.NamedTemporaryFile(mode='w+b')

tee = subprocess.Popen(["tee", _TEMP_STDOUT ], stdin=subprocess.PIPE)
SAVE = sys.stdout.fileno()

def redirect_file():
    time.sleep(1)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())


    
def get_log():
    data=[]
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    os.dup2(SAVE, sys.stdout.fileno())

    tee.terminate()
    
    with open (_TEMP_STDOUT,"r") as f:
        contents = f.readlines()
        for line in contents:
            line = line.strip()
            if line == "":
                pass
            else:
                data.append(line)
    return data
    
def check_host_os():
    """ check and return the type of host operating system """
    if platform.system().startswith("Windows"):
        return"Windows"
    elif platform.system().startswith("Linux"):
        return "Linux"
    else:
        return "UNKNOWN"

def remove_comments(line):
    """remove # comments from given line """
    i = line.find("#")
    if i >= 0:
        line = line[:i]
    return line.strip()

def strip_quotes(value):
    """strip both single or double quotes"""
    value = value.strip()
    if "\"" in value:
        return value.strip("\"")
    elif "\'" in value:
        return value.strip("\'")
    else:
        return value

def boolean_filter(value):

    """ try to determine if give string match boolean type
        @return boolean if the value matches
        @return the original value if not match
    """

    value = strip_quotes(value)
    
    if value in ["TRUE","True","true","1"]:
        return True
    elif value in ["FALSE","False","false","0"]:
        return False
    else:
        return value
        

