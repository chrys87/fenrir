#!/usr/bin/python

import configparser
import os
import sys
from os import listdir
from os.path import isfile, join
from inspect import isfunction
from xdg import BaseDirectory

# Get configuration directory
if len(sys.argv) > 1:
    configPath = sys.argv[1]
else if os.geteuid() == 0:
    # Save settings system wide
    configPath = "/etc"
else
    # Use local settings
    configPath = BaseDirectory.xdg_config_data + "/fenrir"


