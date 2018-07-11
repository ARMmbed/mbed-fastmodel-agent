[![Coverage Status](https://coveralls.io/repos/github/jamesbeyond/mbed-fastmodel-agent/badge.svg?branch=master)](https://coveralls.io/github/jamesbeyond/mbed-fastmodel-agent?branch=master)

# mbed-fastmodel-agent

mbed-fastmodel-agent is a python module for mbed os testing framework using FastModels FVP(Fixed Virtual Platforms).

This module enables [greentea](https://github.com/ARMmbed/greentea) and [htrun](https://github.com/ARMmbed/htrun) running mbed os tests on Fast Models 

To use this module, It is required FastModel and it's PyCADI interface to be installed on the host.

## download
```
git clone <repo_address>
cd mbed-fastmodel-agent
```

## configurations
1. Make sure you have Arm FastModels product installed, and "PVLIB_HOME" environment variable is set.
2. Edit the "Global" section in file `fm_agent\settings.json` 
3. Change "model_lib_path" to your fastmodel installation folder (where contains all fastmodel libs).
4. Optional: edit individual models if necessary
4. Optional: add configs to models if necessary

## install
```
python setup.py install
```
*NOTE. you will need to re-run the install command after you changed the "settings.json" or any config file*

## usage

### Self test if fastmodel product installed correctly, "PVLIB_HOME" and PyCADI are avaliable
```
    mbedfm --self-test
``` 

### list available models you can use with mbed testing framwork
```
    mbedfm
``` 

### run mbed test with greentea
```
    mbedgt --fm <model_name>:<config_name>
```    
*e.g. mbedgt --fm FVP_MPS2_M3:DEFAULT*

*model_name  : The name to fastmodel target supported in mbed os*

*config_name : This could be ether pre-defined CONFIG_NAME listed inside mbedfm or a local file*
 


### run mbed test with htrun
```
    mbedhtrun --fm <config_name> -m <model_name> -f <test_image>
``` 
*e.g. mbedhtrun --fm DEFAULT -m FVP_MPS2_M3*
   
*model_name  : The name to fastmodel target supported in mbed os*

*config_name : This could be ether pre-defined CONFIG_NAME listed inside mbedfm or a local file*

## Known issues:
1. Fast Models normally have 3 or 4 serial terminal ports. But currently only one port is supported at moment. Port number is picked randomly.