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

import json
import os.path
import os
from .utils import SimulatorError, getenv_replace

class FastmodelConfig():

    # default settings file
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        """ initialization of FastmodelConfig """

        settings_json_file = os.path.join(os.path.dirname(__file__), self.SETTINGS_FILE)

        with open(settings_json_file,"r") as config_json:
            self.json_configs = json.load(config_json)

    def get_all_configs (self):
        """ search every config for all the models in SETTINGS_FILE
            @return a dictionary for configs and models combination
        """
        all_config_dict={}
        for model in self.json_configs.keys():
            if model != "COMMON":
                all_config_dict[model]=self.get_configs(model)

        return all_config_dict

    def get_IRIS_path(self):
        """ get the IRIS path from the config file
            @return IRIS path if setting exist
            @return None if not exist
        """
        if "IRIS_path" in self.json_configs["COMMON"]:
            return getenv_replace(self.json_configs["COMMON"]["IRIS_path"])
        else:
            return None

    def get_model_binary(self,model_name):
        """ get the model binary path and name from the config file
            @return full name and path to the model_binary
            @return None if not exist
        """
        if model_name not in self.json_configs:
            return None

        if "model_binary" not in self.json_configs[model_name]:
            return None

        return getenv_replace(self.json_configs[model_name]["model_binary"])

    def get_model_options(self,model_name):
        """ get the model binary options from the config file
            @return a list of model options
            @return an empty list if not found
        """
        if model_name not in self.json_configs:
            return []

        if "model_options" not in self.json_configs[model_name]:
            return []

        return self.json_configs[model_name]["model_options"]

    def get_model_terminal_comp(self,model_name):
        """ get the model terminal compoment name from the config file
            @return full name to model terminal compoment
            @return None if not exist
        """
        if model_name not in self.json_configs:
            return None

        if "terminal_component" not in self.json_configs[model_name]:
            return None

        return self.json_configs[model_name]["terminal_component"]

    def get_configs (self,model_name):
        """ Search for configs with given model
            @return a dictionary of config_name:config_file for give model_name
            @return None if no config found
        """
        if model_name not in self.json_configs:
            return None

        if "configs" in self.json_configs[model_name]:
            local_configs = self.json_configs[model_name]["configs"].copy()
            return local_configs
        elif "configs_add" in self.json_configs[model_name]:
            global_configs  = self.json_configs["COMMON"]["configs"].copy()
            addtion_configs = self.json_configs[model_name]["configs_add"].copy()
            return dict(global_configs,**addtion_configs)
        else:
            global_configs  = self.json_configs["COMMON"]["configs"].copy()
            return global_configs

