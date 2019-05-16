[![Coverage Status](https://coveralls.io/repos/github/jamesbeyond/mbed-fastmodel-agent/badge.svg?branch=master)](https://coveralls.io/github/jamesbeyond/mbed-fastmodel-agent?branch=master)

# mbed-fastmodel-agent

mbed-fastmodel-agent is a python module for Mbed OS GreenTea testing framework using FastModels FVP (Fixed Virtual Platforms).

This module only designed to work with [Greentea](https://github.com/ARMmbed/mbed-os-tools/tree/master/packages/mbed-greentea) and [Htrun](https://github.com/ARMmbed/mbed-os-tools/tree/master/packages/mbed-host-tests),
It enables enables Fast Models to run Mbed OS Greentea test suites. 

If user only need to run mbed OS applications or examples rather than Greentea tests on Fast Models, please referencing [this mbed OS documents](https://os.mbed.com/docs/v5.10/tools/fast-models.html)


## Requirements
 1. Make sure you have Arm Fast Models Libraries files installed to your host machines, as well as the Fast Models PyCADI.

>please referencing [Fast Models User Guide](https://developer.arm.com/docs/100965/latest)

 2. A valid Fast Models license been set up correctly.

>please referencing [Fast Models User Guide](https://developer.arm.com/docs/100965/latest)

 3. Greentea version 1.5.0 or later
```
pip install mbed-greentea -U
mbedgt --version
```
 4. Htrun version 1.4.1 or later
```
pip install mbed-host-tests -U
mbedhtrun --version
```

## Download
```
git clone https://github.com/ARMmbed/mbed-fastmodel-agent.git
cd mbed-fastmodel-agent
```

## Settings before installation
1. Edit the configuration file `fm_agent\settings.json` 
2. Change `model_lib_path` value in the `GLOBAL` section to your Fast Models installation folder (where contains all fastmodel libs).
3. Change `PyCADI_path` value to PyCADI folder, alternatively you can have `PVLIB_HOME` environment variable set on your host
4. Optional: edit individual models if necessary
5. Optional: add configs to models if necessary

## Installation
```
python setup.py install
```
*NOTE. you will need to re-run the install command after you changed the "settings.json" or any config file*

## Basic usage

### list available models you can use with mbed testing framework
```
    mbedfm
```
you should be able to see a table like:
```
+--------------+-----------------------------------------------+-------------+--------------+--------------+
| MODEL NAME   | MODEL LIB full path                           | CONFIG NAME | CONFIG FILE  | AVAILABILITY |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
|              |                                               | DEFAULT     | DEFAULT.conf | YES          |
| FVP_MPS2_M0  | C:\work\model_libs\FVP_MPS2_Cortex-M0.dll     | FAST        | FAST.conf    | YES          |
|              |                                               | NETWORK     | NETWORK.conf | YES          |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
|              |                                               | DEFAULT     | DEFAULT.conf | YES          |
| FVP_MPS2_M0P | C:\work\model_libs\FVP_MPS2_Cortex-M0plus.dll | FAST        | FAST.conf    | YES          |
|              |                                               | NETWORK     | NETWORK.conf | YES          |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
|              |                                               | DEFAULT     | DEFAULT.conf | YES          |
| FVP_MPS2_M3  | C:\work\model_libs\FVP_MPS2_Cortex-M3.dll     | FAST        | FAST.conf    | YES          |
|              |                                               | NETWORK     | NETWORK.conf | YES          |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
|              |                                               | DEFAULT     | DEFAULT.conf | YES          |
| FVP_MPS2_M4  | C:\work\model_libs\FVP_MPS2_Cortex-M4.dll     | FAST        | FAST.conf    | YES          |
|              |                                               | NETWORK     | NETWORK.conf | YES          |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
|              |                                               | DEFAULT     | DEFAULT.conf | YES          |
| FVP_MPS2_M7  | C:\work\model_libs\FVP_MPS2_Cortex-M7.dll     | FAST        | FAST.conf    | YES          |
|              |                                               | NETWORK     | NETWORK.conf | YES          |
+--------------+-----------------------------------------------+-------------+--------------+--------------+
```
### Self test for the settings
```
    mbedfm --self-test
```
This command will check if Fast Models product installed correctly and if mbed-fastmodel-agent module been configured correctly
This will try to launch every model in the above list to verify them, so will take some time to finish

### run mbed Greentea test
```
    mbedgt --fm <model_name>:<config_name>
```
>e.g. `mbedgt --fm FVP_MPS2_M3:DEFAULT`

### run mbed test with htrun
```
    mbedhtrun --fm <config_name> -m <model_name> -f <test_image>
```
>e.g. `mbedhtrun --fm DEFAULT -m FVP_MPS2_M3 -f test.elf`

*<model_name> : The name to fastmodel target supported in mbed os*

*<config_name> : This could be ether pre-defined `CONFIG_NAME` listed inside mbedfm or a local file*

# Configurations to Fast Models

The mbed fastmodel_agent module allow user to configure each individual module via a config file.
by default, 3 config files are provided:
* DEFAULT - default settings
* FAST - based on default turned off speed limit 
* NETWORK - based on default enabled Ethernet

## change config files

all config files are in `mbed-fastmodel-agent\fm_agent\configs` directory, user can edit config file if required.

The config files are standard Fast Models config file. for more detail about details of the settings, please check [Fast Models Users guide](https://developer.arm.com/docs/100965/latest)
*NOTE. you will need to re-run the install command after you changed the "settings.json" or any config file*

## Add your own config file

Users are able to add their own customized config file to the `mbed-fastmodel-agent\fm_agent\configs` directory.

Then users need to edit `mbed-fastmodel-agent\fm_agent\settings.json` file either in `GLOBAL` section or individual models.

Key `configs_add` can be added for additional config files for each model, Or Key `config` can be added to overwrite `GLOBAL` config files.

## Known limitations:
1. Fast Models normally have 3 or 4 serial terminal ports. But currently only one port is used at moment.

