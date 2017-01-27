#!/bin/python
# -*- coding: utf-8 -*-
# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
import sys
version = sys.version[:3] # we only need major.minor version.
if version in ["3.3","3.4"]:
    from importlib.machinery import SourceFileLoader
else: # Python 3.5+, no support for python < 3.3.
    import importlib.util

def importModule(moduleName, moduleLocation):
    if version in ["3.3","3.4"]:
        return SourceFileLoader(moduleName, moduleLocation).load_module()
    else:
        spec = importlib.util.spec_from_file_location(moduleName, moduleLocation)
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        return driver_mod
