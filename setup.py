"""
This module defines the attributes of the
PyPI package for the mbed SDK test suite
"""

"""
mbed SDK
Copyright (c) 2018-2021 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Qinghao Shi <Qinghao.shi@arm.com>
"""

import os
from io import open
from distutils.core import setup
from setuptools import find_packages


LICENSE = open('LICENSE', encoding="utf-8").read()
DESCRIPTION = "Fast Model Agent for mbed tools: greentea and htrun"
OWNER_NAMES = 'Qingaho Shi'
OWNER_EMAILS = 'Qinghao.Shi@arm.com'

# Utility function to cat in a file (used for the README)
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()

setup(name='mbed-fastmodel-agent',
      version='2.0',
      description=DESCRIPTION,
      long_description=read('README.md'),
      entry_points = {'console_scripts': ['mbedfm=fm_agent.mbedfm:main']},
      author=OWNER_NAMES,
      author_email=OWNER_EMAILS,
      maintainer=OWNER_NAMES,
      maintainer_email=OWNER_EMAILS,
      url='https://github.com/ARMmbed/mbed-fastmodel-agent',
      packages=find_packages(),
      license=LICENSE,
      test_suite = 'test',
      include_package_data=True,
      install_requires=[
          "PrettyTable>=0.7.2",
          "mbed-host-tests>=1.5.0",
          "mbed-greentea>=1.5.0"
      ]
)

