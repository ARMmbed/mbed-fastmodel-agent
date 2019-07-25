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

import sys
import os
from fm_agent import FastmodelAgent
from fm_agent import SimulatorError
from fm_agent import check_import
from prettytable import PrettyTable
import argparse


def get_version():
    """! Get fm_agent Python module version string """
    import pkg_resources  # part of setuptools
    return pkg_resources.require("mbed-fastmodel-agent")[0].version

def print_version():
    print(get_version())

def print_models():
    print(list_fastmodels())
    print("Import PyCADI Test ... {}".format("PASSED" if check_import() else "FAILED"))

def self_test():
    print(list_fastmodels(check_models=True))
    print("Import PyCADI Test ... {}".format("PASSED" if check_import() else "FAILED"))  

def list_fastmodels(check_models=False):
    """! List all models and configs in fm_agent"""
    
    resource = FastmodelAgent()
    model_dict = resource.list_avaliable_models()

    columns = ['MODEL NAME', "MODEL LIB full path", 'CONFIG NAME' , 'CONFIG FILE', 'AVAILABILITY']
    if check_models:
        columns.append('SELF TEST')

    pt = PrettyTable(columns)
    pt.hrules =  1

    for col in columns:
        pt.align[col] = 'l'

    for model_name, configs in sorted(model_dict.items()):
        lib_path = resource.list_model_lib(model_name)

        c_names_cell=[]
        c_files_cell=[]
        c_avail_cell=[]
        if check_models:
            c_test_cell=[]

        for config_name, config_file in sorted(configs.items()):
            c_names_cell.append(config_name)
            c_files_cell.append(config_file)

        for file in c_files_cell:
            if not os.path.exists(lib_path):
                c_avail_cell.append("NO  'MODEL LIB' NOT EXIST")
                if check_models:
                    c_test_cell.append("SKIPPED")
            elif resource.check_config_exist(file):
                c_avail_cell.append("YES")
                if check_models:
                    try:
                        resource.setup_simulator(model_name,config_name)
                        resource.start_simulator()
                        c_test_cell.append("PASSED" if resource.is_simulator_alive() else "FAILED")
                        resource.shutdown_simulator()
                    except Exception as e:
                        print(str(e))
                        c_test_cell.append("FAILED")
            else:
                c_avail_cell.append("NO  'CONFIG FILE' NOT EXIST")
                if check_models:
                    c_test_cell.append("SKIPPED")

        MAX_WIDTH = 60
        lib_path_cell = [lib_path[i:i+MAX_WIDTH] for i in range(0, len(lib_path), MAX_WIDTH)]
        
        padding_lines_col1 = "\n" * ((len(c_names_cell)-1) // 2)
        padding_lines_col2 = "\n" * ((len(c_names_cell)-len(lib_path_cell)) // 2)
        
        row_list = [padding_lines_col1+model_name,
                    padding_lines_col2+"\n".join(lib_path_cell),
                    "\n".join(c_names_cell),
                    "\n".join(c_files_cell),
                    "\n".join(c_avail_cell)]
        if check_models:
            row_list.append("\n".join(c_test_cell))  

        pt.add_row(row_list)

    return pt.get_string()
    
def cli_parser(in_args):
    """parser for command line options"""
    parser = argparse.ArgumentParser(description='fastmodel agent command line interface.')
    parser.set_defaults(command=print_models)
    parser.add_argument('-v', '--version', dest='command',
                        action='store_const', const=print_version,
                        help='print package version and exit')
    parser.add_argument('-t', '--self-test', dest='command',
                        action='store_const', const=self_test,
                        help='self-test if fast model can be launch successfully')
    out_args = parser.parse_args(in_args)
    return out_args
    
def main():
    args = cli_parser(sys.argv[1:])
    ret_code = args.command()
    if not ret_code:
        ret_code = 0
    sys.exit(ret_code)

