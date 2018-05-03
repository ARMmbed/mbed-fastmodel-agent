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

import json
import os.path
from .utils import check_host_os
from .utils import remove_comments
from .utils import boolean_filter

class configError(Exception):
    """
    Resource specific fastmodel AgentError
    """
    pass

class FastmodelConfig():
    
    # default configration file
    CONFIG_FILE = "config.json"
            
    def __init__(self):
        """ initialization of FastmodelConfig """
        
        main_json_file = os.path.join(os.path.dirname(__file__) , self.CONFIG_FILE)

        with open(main_json_file,"r") as config_json:    
            self.json_configs = json.load(config_json)
        self.os = check_host_os();
        
    def get_all_configs (self):
        """ search every config for all the models in CONFIG_FILE
            @return a dictionary for configs and models combination
        """

        all_config_dict={}
        for model in self.json_configs.keys():
            if model != "GLOBAL":
                all_config_dict[model]=self.get_configs(model)

        return all_config_dict
        
    def get_model_lib(self,model_name):
        """ get the model lib path and name from the config file
            @retrun full name and path to the model_lib
            @return None if not exist
        """

        if model_name not in self.json_configs:
            return None

        if "model_lib" not in self.json_configs[model_name][self.os]:
            return None

        model_lib_name  = self.json_configs[model_name][self.os]["model_lib"]   

        if "model_lib_path" in self.json_configs[model_name][self.os]:
            local_path = self.json_configs[model_name][self.os]["model_lib_path"]
            return str(os.path.join( local_path , model_lib_name ))
        else:
            global_path = self.json_configs["GLOBAL"][self.os]["model_lib_path"]
            return str(os.path.join( global_path , model_lib_name ))

    def get_configs (self,model_name):
        """ Search for configs with given model 
            @return a dictionary of config_name:config_file for give model_name
            @return None if no config found
        """

        if model_name not in self.json_configs:
            return None

        if "configs" in self.json_configs[model_name][self.os]:
            local_configs = self.json_configs[model_name][self.os]["configs"].copy()
            return local_configs
        elif "configs_add" in self.json_configs[model_name][self.os]:
            global_configs  = self.json_configs["GLOBAL"][self.os]["configs"].copy()
            addtion_configs = self.json_configs[model_name][self.os]["configs_add"].copy()
            return dict(global_configs,**addtion_configs)
        else:
            global_configs  = self.json_configs["GLOBAL"][self.os]["configs"].copy()
            return global_configs        

    def parse_params_file (self, config_file , in_module=True):
        """ read fastmodel parameters from given config_file
            @param config_file need to be file name only
            @param in_module default is True, means the config_file inside module folder
            @param if in_module set to False, will looking for config_file in pwd
            @return if config_file read failed, function will throw configError
            @return if config_file format is wrong, function will throw configError
            @return if config_file been parsed successfully, will return a dictionary of parameters 
        """

        if in_module:
            filepath = os.path.join( os.path.dirname(__file__) , config_file )
        else:
            filepath = os.path.join( os.getcwd() , config_file )
            
        if not os.path.exists(filepath):
            raise configError("model config file not exit: %s" % filepath)
            return None
        
        params_dict={}
        with open(filepath,'r') as CONF_file: 
            param_data = CONF_file.readlines()
        for line in param_data:
            line = remove_comments(line)
            if line:
                if line.count("=")==0:
                    raise configError("Wrong format in config %s,\nline %s should match format key=values" % (filepath,line))
                    return None
                elif line.count("=")>1:
                    raise configError("Wrong format in config %s,\nline %s having more than one '='" % (filepath,line))
                    return None
                elif line.startswith("="):
                    raise configError("Wrong format in config %s,\nline %s should match format key=values" % (filepath,line))
                    return None
                elif line.endswith("="):
                    raise configError("Wrong format in config %s,\nline %s should match format key=values" % (filepath,line))
                    return None
                else:
                    param_key,param_value = line.split("=")
                    params_dict[param_key.strip()] = boolean_filter(param_value) 
                    
        return params_dict
