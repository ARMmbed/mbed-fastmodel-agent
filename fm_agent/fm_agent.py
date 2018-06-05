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
import time
import socket
import logging
from .utils import *
from .fm_config import FastmodelConfig

class FastmodelAgent():
    def __init__(self, model_name=None, model_config=None, logger=None):
        """ initialize FastmodelAgent
            @param all are optional, if none of the argument give, will just query for information 
            @param if want to launch and connect to fast model, model_name and model_config are necessary
            @param model_name is the name to the fast model
            @param model_config is the config file to the fast model
        """
        
        self.fastmodel_name = model_name
        self.config_name    = model_config

        #If logging not provided, use default log
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('fastmodel-agent')
            if not self.logger.handlers:
                self.logger.addHandler(logging.NullHandler())
            self.logger.setLevel(logging.ERROR)
            self.logger.propagate = False
            self.logger.info('No logger supplied, using default logging logger')

        self.read_timeout = 0.2
        self.model = None # running instant of the model
        self.socket = None # running instant of socket
        self.configuration = FastmodelConfig()

        if model_config:
            self.__run_mode()
        else:
            pass

    def __run_mode(self):
        if not self.fastmodel_name:
            self.logger.prn_err("Please provided the name to a fastmodel!!")
            self.__guide()
            raise SimulatorError("fastmodel_name not provided!")
        self.model_lib = self.configuration.get_model_lib(self.fastmodel_name)

        if not self.model_lib:
            self.logger.prn_err("NO model_lib available for '%s'"% self.fastmodel_name)
            self.__guide()
            raise SimulatorError("fastmodel '%s' not available" % (self.fastmodel_name))
            
        config_dict = self.configuration.get_configs(self.fastmodel_name)
        
        if config_dict and self.config_name in config_dict:
            self.model_params = self.configuration.parse_params_file(config_dict[self.config_name])
        elif os.path.exists(os.path.join( os.getcwd(), self.config_name )):
            self.model_params = self.configuration.parse_params_file(self.config_name,in_module=False)
        else:
            self.__guide()
            raise SimulatorError("No config %s avaliable for fastmodel %s" % (self.config_name,self.fastmodel_name))
            
    def __connect_terminal(self):
        """ connect socket terminal to a launched fastmodel"""

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
        
    def start_simulator(self):
        """ launch given fastmodel with configs """
        if check_import():
            import fm.debug
            # try to detect free port for launch terminal, This should be changed to redirect stdout later on
            self.port = find_free_port()
            self.host = "localhost"
            self.model_params.update({"fvp_mps2.telnetterminal0.start_port":self.port,
                                      "fvp_mps2.telnetterminal1.start_port":self.port,
                                      "fvp_mps2.telnetterminal2.start_port":self.port})
            # module launch parameters
            self.model = fm.debug.LibraryModel(self.model_lib, self.model_params)
            return True
        else:
            raise SimulatorError("fastmodel product was NOT installed correctly")

    def load_simulator(self,image):
        """ Load a launched fastmodel with given image(full path)"""
        if self.is_simulator_alive():
            cpu = self.model.get_cpus()[0]
            cpu.load_application(os.path.normpath(image))
            return True
        else:
            return False
        
    def run_simulator(self):
        """ Start running a launched fastmodel and connect terminal """
        if self.is_simulator_alive():
            self.model.run(blocking=False,timeout=1)
            self.__connect_terminal()
            return True
        else:
            return False

    def read(self):
    
        if not self.__socketConnected():
            return None
        
        data = str()
        read_stop = False

        while not read_stop:
            try:
                char=''
                char = self.socket.recv(1)
            except socket.timeout as eto:
                read_stop=True
            except socket.error as e:
                self.socket = None
                self.logger.prn_err("Fastmodel Read connection lost, socket.recv()")
                self.logger.prn_err(str(e))
            else:
                data += char
                if char == "\n":
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
                self.socket.sendall(char)
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

    def shutdown_simulator(self):
        """ shutdown fastmodel if any """
        if self.is_simulator_alive():
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

    def list_model_lib(self, model_name):
        """ return model lib full path of give model_name """
        return self.configuration.get_model_lib(model_name)
        
    def check_config_exist(self,filename):
        """ return the presents of give config name
        """

        filepath = os.path.join( os.path.dirname(__file__), "configs" , filename )

        return os.path.exists(filepath)


