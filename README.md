[![Coverage Status](https://coveralls.io/repos/github/jamesbeyond/mbed-fastmodel-agent/badge.svg?branch=master)](https://coveralls.io/github/jamesbeyond/mbed-fastmodel-agent?branch=master)

# mbed-fastmodel-agent

mbed-fastmodel-agent is a python module for Mbed OS GreenTea testing framework using FastModels FVP (Fixed Virtual Platforms).

This module only designed to work with [Greentea](https://github.com/ARMmbed/mbed-os-tools/tree/master/packages/mbed-greentea) and [Htrun](https://github.com/ARMmbed/mbed-os-tools/tree/master/packages/mbed-host-tests),
It enables enables Fast Models to run Mbed OS Greentea test suites. 

If user only need to run mbed OS applications or examples rather than Greentea tests on Fast Models, please referencing [this mbed OS documents](https://os.mbed.com/docs/v5.10/tools/fast-models.html)


## Requirements
 1. Make sure you have Arm Fast Models FVPs as well as the Fast Models Iris python modules installed. This Package is not including neither of them. Also a valid license to the Fastmodels could be required.

>please referencing [Fast Models User Guide](https://developer.arm.com/docs/100965/latest)

 2. Use Greentea and mbedhtrun version 1.5.0 or later
```
# Check versions
mbedgt --version
mbedhtrun --version

# Update mbedgt and mbedhtrun
pip install mbed-greentea -U
pip install mbed-host-tests -U
```

## Download
```
git clone https://github.com/ARMmbed/mbed-fastmodel-agent.git
cd mbed-fastmodel-agent
```

## Configurations before installation
1. Edit the configuration file `fm_agent\settings.json` 
3. Change `IRIS_path` value to IRIS Python folder
3. Edit individual models binarys file path
4. Optional: customize configs to models

## Installation
```
sudo python setup.py install
```
*NOTE. you will need to re-run the install command after you changed the "settings.json" or any config file*

## Basic usage

### list available models you can use with mbed testing framework
```
    mbedfm
```
you should be able to see a table like:
```
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| MODEL NAME   | MODEL Binary Full Path                        | CONFIG NAME | CONFIG FILE   | AVAILABILITY |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| FVP_MPS2_M0  | C:\work\models\FVP_MPS2_Cortex-M0.exe         | MPS2        | MPS2.conf     | YES          |
|              |                                               | COVERAGE    | COVERAGE.conf | YES          |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| FVP_MPS2_M0P | C:\work\models\FVP_MPS2_Cortex-M0plus.exe     | MPS2        | MPS2.conf     | YES          |
|              |                                               | COVERAGE    | COVERAGE.conf | YES          |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| FVP_MPS2_M3  | C:\work\models\FVP_MPS2_Cortex-M3.exe         | MPS2        | MPS2.conf     | YES          |
|              |                                               | COVERAGE    | COVERAGE.conf | YES          |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| FVP_MPS2_M4  | C:\work\models\FVP_MPS2_Cortex-M4.exe         | MPS2        | MPS2.conf     | YES          |
|              |                                               | COVERAGE    | COVERAGE.conf | YES          |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
| FVP_MPS2_M7  | C:\work\models\FVP_MPS2_Cortex-M7.exe         | MPS2        | MPS2.conf     | YES          |
|              |                                               | COVERAGE    | COVERAGE.conf | YES          |
+--------------+-----------------------------------------------+-------------+---------------+--------------+
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
>e.g. `mbedgt --fm FVP_MPS2_M3:MPS2`

### run mbed test with htrun
```
    mbedhtrun --fm <config_name> -m <model_name> -f <test_image> <-e host_test_path>
```
>e.g. `mbedhtrun -m FVP_MPS2_M3  --fm MPS2 -f test.elf -e ./host_tests`

*<model_name> : The name to fastmodel target supported in mbed os*

*<config_name> : This could be ether pre-defined `CONFIG_NAME` listed inside mbedfm or a local file*

# Configurations to Fast Models

The mbed fastmodel_agent module allow user to configure each individual module via a config file.
by default, 3 config files are provided:
* MPS2 - default settings for MPS2 based platforms
* MPS3 - default settings for MPS3 based platforms
* COVERAGE - configuration for MPS2 Code Coverage Test 


## change config files

all config files are in `mbed-fastmodel-agent\fm_agent\configs` directory, user can edit config file if required.

The config files are standard Fast Models config file. for more detail about details of the settings, please check [Fast Models Users guide](https://developer.arm.com/docs/100965/latest)
*NOTE. you will need to re-run the install command after you changed the "settings.json" or any config file*

## Add your own config file

Users are able to add their own customized config file to the `mbed-fastmodel-agent\fm_agent\configs` directory.

Then users need to edit `mbed-fastmodel-agent\fm_agent\settings.json` file either in `COMMON` section or individual models.

Key `configs_add` can be added for additional config files for each model, Or Key `config` can be added to overwrite `COMMON` config files.

## Known limitations:
1. Fast Models normally have 3 or 4 serial terminal ports. But currently only one port is used at moment.

