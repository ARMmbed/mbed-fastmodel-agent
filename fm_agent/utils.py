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
import socket
import logging
import subprocess
from functools import partial

class SimulatorError(Exception):
    """
    Simulator specific Error
    """
    pass

class FMLogger(object):
    """! Yet another logger flavour """
    def __init__(self, name, lv=logging.INFO):
        logging.basicConfig(stream=sys.stdout,format='[%(created).2f][%(name)s]%(message)s', level=lv)
        self.logger = logging.getLogger(name)
        self.format_str = '[%(logger_level)s] %(message)s'

        def __prn_log(self, logger_level, text, timestamp=None):
            self.logger.debug(self.format_str% {
                'logger_level' : logger_level,
                'message' : text,
            })

        self.prn_dbg = partial(__prn_log, self, 'DBG')
        self.prn_wrn = partial(__prn_log, self, 'WRN')
        self.prn_err = partial(__prn_log, self, 'ERR')
        self.prn_inf = partial(__prn_log, self, 'INF')
        self.prn_txt = partial(__prn_log, self, 'TXT')
        self.prn_txd = partial(__prn_log, self, 'TXD')
        self.prn_rxd = partial(__prn_log, self, 'RXD')    

def get_PyCADI_path(self):
    """ get the PyCADI path from the config file
        @return PyCADI path if setting exist 
        @return None if not exist
    """
    if "PyCADI_path" in self.json_configs["GLOBAL"]:
        return self.json_configs["GLOBAL"][self.os]["PyCADI_path"]
    else:
        return None
        
def check_import():
    """ Append PVLIB_HOME to PATH, so import PyCADI fm.debug can be imported """
    warning_msgs = []
    from .fm_config import FastmodelConfig
    config = FastmodelConfig()

    fm_pycadi_path = config.get_PyCADI_path()
    if fm_pycadi_path:
        if os.path.exists(fm_pycadi_path):
            sys.path.append(fm_pycadi_path)
        else:
            warning_msgs.append("Warning: Could not locate PyCADI_path '%s'" % fm_pycadi_path)
    else:
        warning_msgs.append("Warning: PyCADI_path not set in settings.json")
    
    if 'PVLIB_HOME' in os.environ:
        #FastModels PyCADI have different folder on different host OS
        fm_pycadi_path1 = os.path.join(os.environ['PVLIB_HOME'], 'lib', 'python27')
        fm_pycadi_path2 = os.path.join(os.environ['PVLIB_HOME'], 'lib', 'python2.7')
        if os.path.exists(fm_pycadi_path1):
            sys.path.append(fm_pycadi_path1)
        elif os.path.exists(fm_pycadi_path2):
            sys.path.append(fm_pycadi_path2)
        else:
            warning_msgs.append("Warning: Could not locate PyCADI in PVLIB_HOME/lib/python27")
    else:
        warning_msgs.append("Warning: 'PVLIB_HOME' environment variable not been set.")

    try:
        import fm.debug
    except ImportError as e:
        for warning in warning_msgs:
            print(warning)
        print("Error: Failed to import fast models PyCADI!!!")
        return False
    else:
        return True
    
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

def find_free_port():
    """try to determine a free random port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    addr, port = s.getsockname()
    s.close()
    return port

    """ the following function mainly for coverage mode """

def read_symbol(image):
    """this function reads images symbol to a global variable"""
    symbol_table = []
    try:
        symbol_table =  subprocess.check_output('arm-none-eabi-readelf -sW "{}"'.format(image), shell=True).split("\n")
    except Exception as e:
        print("Make sure you have arm-none-eabi-readelf tool in PATH")
        print("ERROR - {}.".format(str(e)))
        sys.exit(1)
    return symbol_table

def get_symbol_addr(symbol_table, symbol_name):
    """
    Num:   Value  Size Type    Bind   Vis      Ndx Name
    24: 0002f45a     0 NOTYPE  LOCAL  DEFAULT    2 init_bss
    25: 0002f470     0 NOTYPE  LOCAL  DEFAULT    2 system_startup
    26: 0002f468     0 NOTYPE  LOCAL  DEFAULT    2 zero
    """
    for line in symbol_table:
        data = line.split()
        if symbol_name in data:
            return data[1]

def ByteToInt( byteList ):
    return int(''.join( [ "{:02x}".format(x) for x in reversed(byteList) ] ),16)

def HexToInt( hex ):
    return int(hex,16)
    
def lcov_collect(filename):
    """this function reads images symbol to a global variable"""
    subprocess.call('lcov -c -d . --no-external -o BUILD/{}.info'.format(filename), shell=True)
        
def remove_gcda(rootdir="."):
    """this function removes gcda files"""
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".gcda"):
                os.remove(os.path.join(root, file))
