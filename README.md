# mbed-fastmodel-agent

mbed-fastmodel-agent is a python module for mbed os testing framework using FastModels FVP(Fixed Virtual Platforms).

This module enables [greentea](https://github.com/ARMmbed/greentea) and [htrun](https://github.com/ARMmbed/htrun) running mbed os tests on Fast Models 

This module also need FastModel and it's PyCADI to be installed on the host.

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

### list available models you can use with mbed testing framwork
```
    mbedfm
``` 

### run mbed test with greentea
```
    mbedgt --srm <model_name>:fm_agent:<config_name>
```    
*e.g. mbedgt --srm FVP_MPS2_M3:fm_agent:DEFAULT*

*model_name  : The name to fastmodel target supported in mbed os*

*config_name : This could be ether pre-defined CONFIG_NAME listed inside mbedfm or a local file*
 


### run mbed test with htrun
```
    mbedhtrun --srm fm_agent:<config_name> -m <model_name> -f <test_image>
``` 
*e.g. mbedhtrun --srm fm_agent:DEFAULT -m FVP_MPS2_M3*
   
*model_name  : The name to fastmodel target supported in mbed os*

*config_name : This could be ether pre-defined CONFIG_NAME listed inside mbedfm or a local file*

## Known issues:
1. currently not supporting running multiple fast_models at same time due to model serial port is hard coded at 5000