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

import sys
import os
import time
import socket
from .utils import *
from .fm_config import FastmodelConfig

_GDB_PORT = 31627

class FastmodelAgent():
    def __init__(self, model_name=None, model_config=None, logger=None, enable_gdbserver=False):
        """ initialize FastmodelAgent
            @param all are optional, if none of the argument give, will just query for information
            @param if want to launch and connect to fast model, model_name and model_config are necessary
            @param model_name is the name to the fast model
            @param model_config is the config file to the fast model
        """

        self.fastmodel_name = model_name
        self.config_name    = model_config
        self.enable_gdbserver = enable_gdbserver
        self.subprocess = None

        #If logging not provided, use default log
        if logger:
            self.logger = logger
        else:
            self.logger = FMLogger('fm_agent')

        self.read_timeout = 0.2
        self.model = None # running instant of the model
        self.socket = None # running instant of socket
        self.configuration = FastmodelConfig()

        if model_config:
            self.setup_simulator(model_name,model_config)
        else:
            pass

    def setup_simulator(self, model_name, model_config):
        """ setup the simulator, this is crucial before you can start a simulator.
            @param model_name is the specific model name need to be launched
            @param model_config is the specific model configure file need to be launched
            This function check if both model_name or model_config are valid
        """
        self.fastmodel_name = model_name
        self.config_name    = model_config

        if not self.fastmodel_name:
            self.logger.prn_err("Please provided the name to a fastmodel!!")
            self.__guide()
            raise SimulatorError("fastmodel_name not provided!")
        self.model_binary = self.configuration.get_model_binary(self.fastmodel_name)

        if not self.model_binary:
            self.logger.prn_err("NO model_binary available for '%s'"% self.fastmodel_name)
            self.__guide()
            raise SimulatorError("fastmodel '%s' not available" % (self.fastmodel_name))

        self.model_options = self.configuration.get_model_options(self.fastmodel_name)
        if self.enable_gdbserver:
            global _GDB_PORT
            self.gdb_port = _GDB_PORT
            _GDB_PORT += 1

            self.model_options += [
                '--allow-debug-plugin',
                '--plugin',
                'GDBRemoteConnection.so',
                '-C',
                f'REMOTE_CONNECTION.GDBRemoteConnection.port={self.gdb_port}'
            ]


        config_dict = self.configuration.get_configs(self.fastmodel_name)

        if config_dict and self.config_name in config_dict:
            config_file = config_dict[self.config_name]
            self.model_config_file = os.path.join( os.path.dirname(__file__) ,"configs" , config_file )

        elif os.path.exists(os.path.join( os.getcwd(), self.config_name )):
            self.model_config_file = os.path.join( os.getcwd() , self.config_name )
        else:
            self.__guide()
            raise SimulatorError("No config %s avaliable for fastmodel %s" % (self.config_name,self.fastmodel_name))

        self.model_terminal = self.configuration.get_model_terminal_comp(self.fastmodel_name)

        if not self.model_terminal:
            self.logger.prn_err("NO terminal_compoment defined for '%s'"% self.fastmodel_name)
            raise SimulatorError("fastmodel '%s' not defined terminal compoment" % (self.fastmodel_name))

    def __connect_terminal(self):
        """ connect socket terminal to a launched fastmodel"""
        self.logger.prn_inf("Establishing socket connection to FastModel Terminal")
        time.sleep(2)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(self.read_timeout)
        except socket.error as e:
            self.socket = None
            self.logger.prn_err("Socket connection error, socket.connect(%s, %s)" % (self.host, self.port))
            self.logger.prn_err("Error: %s" % str(e))

    def __guide(self):
        """ print out information mebdls, help user to spot where possible went wrong"""
        self.logger.prn_inf("Use 'mbedfm' to list all the available Fast Models")

    def is_simulator_alive(self):
        """return if the terminal socket is connected"""
        return bool(self.model)

    def start_simulator(self, stream=sys.stdout):
        """ launch given fastmodel with configs """
        if check_import():
            import iris.debug
            self.subprocess, IRIS_port, outs = launch_FVP_IRIS(self.model_binary, self.model_config_file, self.model_options)
            if stream:
                print(outs, file=stream)
            self.model = iris.debug.NetworkModel('localhost',IRIS_port)
            # check which host socket port is used for terminal0
            terminal = self.model.get_target(self.model_terminal)
            self.port = terminal.read_register('Default.Port')
            self.host = "localhost"
            self.image = None

            return True
        else:
            raise SimulatorError("fastmodel product was NOT installed correctly")

    def load_simulator(self,image):
        """ Load a launched fastmodel with given image(full path)"""
        if self.is_simulator_alive():
            cpu = self.model.get_cpus()[0]
            app = os.path.normpath(image)
            if os.path.exists(app):
                cpu.load_application(app)
                self.image = os.path.normpath(app)
            else:
                self.logger.prn_err("Image %s not exist while loading to Fast Models" % app)
                return False
            return True
        else:
            return False

    def run_simulator(self):
        """ Start running a launched fastmodel and connect terminal """
        if self.is_simulator_alive():
            cpu = self.model.get_cpus()[0]
            if cpu.is_running:
                self.logger.prn_err("Fast Model already in running state")
            else:
                self.model.run(blocking=False)
            self.__connect_terminal()
            return True
        else:
            return False

    def reset_simulator(self):
        """ reset a launched fastmodel and connect terminal """
        if self.is_simulator_alive():
            self.logger.prn_wrn("STOP and RESTART FastModel")
            self.__closeConnection()
            self.model.release(shutdown=True)
            time.sleep(1)
            import iris.debug

            self.subprocess, IRIS_port, outs = launch_FVP_IRIS(self.model_binary, self.model_config_file)
            if IRIS_port==0:
                print(outs)
                return False
            self.model = iris.debug.NetworkModel('localhost',IRIS_port)
            # check which host socket port is used for terminal0
            terminal = self.model.get_target(self.model_terminal)
            self.port = terminal.read_register('Default.Port')
            cpu = self.model.get_cpus()[0]
            if self.image:
                cpu.load_application(self.image)
                self.logger.prn_wrn("RELOAD new image to FastModel")
            self.model.run(blocking=False)
            self.__connect_terminal()
            self.logger.prn_wrn("Reconnect Terminal")
            return True
        else:
            return False

    def read(self, end='\n', bs=-1):

        if not self.__socketConnected():
            return None

        if bs is None:
            bs = -1

        data = bytearray()
        read_stop = False

        while not read_stop:
            try:
                char=bytearray()
                char = self.socket.recv(1)
            except socket.timeout as eto:
                read_stop=True
            except socket.error as e:
                self.socket = None
                self.logger.prn_err("Fastmodel Read connection lost, socket.recv()")
                self.logger.prn_err(str(e))
            else:
                data += char
                if char == end or (bs >= 0 and len(data) >= bs):
                    read_stop=True

        return data

    def write(self, payload, log=False):
        """! Write payload to terminal socket
            @details due to the characteristic of fastmodel terminal socket.
                the reliable way of sending data over the socket in sending character by character
                and the fastest speed we can send is 100 character per second.
                sending too fast will cause fastmodel terminal overrun.
        """

        if not self.__socketConnected():
            return False

        try:
            for char in payload:
                self.socket.sendall(char.encode())
                time.sleep(0.01)
            if log:
                self.logger.prn_txd(payload)
            return True
        except socket.error as e:
            self.socket = None
            self.logger.prn_err("Fastmodel Write connection lost, socket.write(%s)" % payload )
            self.logger.prn_err(str(e))
            return False

    def __socketConnected(self):
        """return whether the socket serial is connected"""
        return bool(self.socket)

    def __closeConnection(self):
        """ close the terminal socket connection"""
        if self.__socketConnected():
            self.socket.close()
            self.logger.prn_inf("Closing terminal socket connection")
            self.socket = None
        else:
            self.logger.prn_inf("Terminal socket connection already closed")

    def __run_to_breakpoint(self):
        try:
            self.model.run(timeout=15)
        except:
            # On timeout, model hangs
            self.logger.prn_err("ERROR: Timeout reached without stop at breakpoint")
            self.model.stop()
            return False
        else:
            return True

    def __CodeCoverage(self):
        """ runs code coverage dump gcda file """

        self.model.stop()
        cpu = self.model.get_cpus()[0]

        symbol_table = []
        self.logger.prn_inf("Reading symbols from %s" % self.image)
        if self.image:
            symbol_table = read_symbol(self.image)

        data_hex_addr = get_symbol_addr(symbol_table, "__gcov_var__ported")
        data_int_addr = HexToInt(data_hex_addr)
        self.logger.prn_inf("Address for [__gcov_var__ported] is %s" % data_hex_addr )

        dump_hex_addr = get_symbol_addr(symbol_table, "__gcov_close__ported")
        dump_int_addr = HexToInt(dump_hex_addr)
        self.logger.prn_inf("Address for [__gcov_close__ported] is %s" % dump_hex_addr )

        exit_hex_addr = get_symbol_addr(symbol_table, "collect_coverage")
        exit_int_addr = HexToInt(exit_hex_addr)
        self.logger.prn_inf("Address for [collect_coverage] is %s" % exit_hex_addr )



        self.logger.prn_inf("Setting breakpoints...")
        bkpt_dump = cpu.add_bpt_prog( dump_int_addr + 57 )
        bkpt_exit  = cpu.add_bpt_prog( exit_int_addr + 43 )

        self.logger.prn_inf("Removing old gcda files...")
        remove_gcda()

        self.__run_to_breakpoint()
        stopped_loc = cpu.read_register('Core.R15')

        while stopped_loc == bkpt_dump.address :

            start_addr    = ByteToInt( cpu.read_memory( data_int_addr   , size=4 ) )
            end_addr      = ByteToInt( cpu.read_memory( data_int_addr+4 , size=4 ) )
            file_var_addr = ByteToInt( cpu.read_memory( data_int_addr+8 , size=4 ) )

            file_var = r''
            mem_char = " "

            while ord(mem_char) != 0:
                mem_char = cpu.read_memory(file_var_addr)
                file_var += str(mem_char)
                file_var_addr += 1

            filename = file_var.rstrip(' \t\r\n\0')
            self.logger.prn_inf("dumping to " + filename)
            with open(filename, "wb") as f:
                mem = cpu.read_memory(start_addr, count=(end_addr-start_addr))
                f.write(mem)

            if self.__run_to_breakpoint():
                stopped_loc = cpu.read_register('Core.R15')
            else:
                stopped_loc = cpu.read_register('Core.R15')
                break


        if stopped_loc == bkpt_exit.address:
            self.logger.prn_inf("Coverage dump program run to the end.")
        else:
            self.logger.prn_wrn("Coverage dump ended somewhere else!!")
        lcov_collect(os.path.basename(self.image))

    def shutdown_simulator(self):
        """ shutdown fastmodel if any """
        if self.is_simulator_alive():
            if self.config_name == "COVERAGE":
                self.__CodeCoverage()
            self.logger.prn_inf("Fast-Model agent shutting down model")
            self.__closeConnection()
            self.model.release(shutdown=True)
            self.model=None
            time.sleep(1)
        else:
            self.logger.prn_inf("Model already shutdown")

    def list_avaliable_models(self):
        """ return a dictionary of models and configs """
        return self.configuration.get_all_configs()

    def list_model_binary(self, model_name):
        """ return model binary full path of give model_name """
        return self.configuration.get_model_binary(model_name)

    def check_config_exist(self,filename):
        """ return the presents of give config name
        """
        filepath = os.path.join( os.path.dirname(__file__), "configs" , filename )
        return os.path.exists(filepath)
