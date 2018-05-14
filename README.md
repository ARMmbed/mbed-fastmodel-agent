# mbed-fastmodel-agent

FastModel agent is a python module for mbed os testing framework using FastModels FVP(Fixed Virtual Platforms).

This module will need to used together with [greentea](https://github.com/ARMmbed/greentea) [htrun](https://github.com/ARMmbed/htrun) and [mbedls](https://github.com/ARMmbed/mbed-ls).

This module also need FastModel and PyCADI to be installed on the host.

## download
```
git clone <repo_address>
cd mbed-fastmodel-agent
```

## configuration
1. Make sure you have Arm FastModels product installed, and you have "PVLIB_HOME" environment variable is set.
2. Edit the "Global" section in file `fastmodel_agent\config.json` 
3. Change "model_lib_path" to your fastmodel installation folder (where contains all fastmodel libs).
4. Optional: edit individual models if necessary
4. Optional: add configs to models if necessary

## install
```
python setup.py install
```
*NOTE. you will need to re-run the install command after you changed the "config.json"*

## usage

* list available models you can use with mbed testing framwork
```
    mbedls -M fastmodel_agent
``` 

* run mbed test with greentea
```
    mbedgt --srm <model_name>:fastmodel_agent:<config_name>
``` 

* run mbed test with htrun
```
    mbedhtrun --srm fastmodel_agent:<config_name> -m <model_name> -f <test_image>
``` 
## Known issues:
1. currently not supporting running multiple fast_models at same time due to model serial port is hard coded at 5000