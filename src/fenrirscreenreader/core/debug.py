#!/usr/bin/python

from enum import Enum

class debugLevel(Enum):
    DEACTIVE = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    def __int__(self):
        return self.value
    def __str__(self):
        return self.name
