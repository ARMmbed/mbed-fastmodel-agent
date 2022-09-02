#!/usr/bin/env python
"""
mbed SDK
Copyright (c) 2011-2021 ARM Limited

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

import os
import sys
import logging
from functools import partial
import subprocess
from subprocess import Popen, PIPE, STDOUT

ON_POSIX = 'posix' in sys.builtin_module_names

NUM_FVP_UART = 5

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

def check_import():
    """ try PyIRIS API iris.debug can be imported """
    warning_msgs = []
    from .fm_config import FastmodelConfig
    config = FastmodelConfig()

    fm_IRIS_path = config.get_IRIS_path()
    if fm_IRIS_path:
        if os.path.exists(fm_IRIS_path):
            sys.path.append(fm_IRIS_path)
        else:
            warning_msgs.append("Warning: Could not locate IRIS_path '%s'" % fm_IRIS_path)
    else:
        warning_msgs.append("Warning: IRIS_path not set in settings.json")

    try:
        import iris.debug
    except ImportError as e:
        for warning in warning_msgs:
            print(warning)
        print("Error: Failed to import fast models PyCADI!!!")
        return False
    else:
        return True

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

def launch_FVP_IRIS(model_exec, config_file='', model_options=[]):
    """Launch FVP with IRIS Server listening"""
    cmd_line = [model_exec, '-I', '-p']
    cmd_line.extend(model_options)
    if config_file:
        cmd_line.extend(['-f' , config_file])
    logging.info(cmd_line)

    fm_proc = Popen(cmd_line, stdout=PIPE, stderr=STDOUT, close_fds=ON_POSIX)

    # Read Iris and telnet terminal ports from stdin. Stop on the first blank line.
    iris_port = None
    terminal_ports = [None]*NUM_FVP_UART
    for line in fm_proc.stdout:
        line = line.strip().decode('utf-8')
        if line == '':
            break

        words = line.split()
        if words[0].startswith('telnetterminal'):
            which = int(words[0][-2])
            terminal_ports[which] = int(words[-1])
        elif words[0].startswith('Iris'):
            iris_port = int(words[-1])

    return (fm_proc, iris_port, terminal_ports)

def getenv_replace(s):
    """Replace substrings enclosed by {{ and }} with values from the environment so that e.g. '{{USER}}' becomes 'root'.
    """
    return s.replace('{{', '{').replace('}}', '}').format(**os.environ)
