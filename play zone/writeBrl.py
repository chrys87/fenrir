#!/bin/python

import brlapi

brl = brlapi.Connection()
print(brl.displaySize)
print(brl.driverName)
try:
    brl.writeText('test')
except Exception as e:
    print(e)
    

