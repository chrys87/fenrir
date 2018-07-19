#!/bin/python3
import argparse

parser = argparse.ArgumentParser(description="Fenrir Help")

parser.add_argument('-s', '--setting', metavar='SETTING-FILE', default='/etc/fenrir/settings/settings.conf', help='Use a specified settingsfile')
parser.add_argument('-o', '--options', metavar='SECTION:SETTING=VALUE,..', default='', help='Overwrite options in given settings file')

args = parser.parse_args()
parser.print_help()

print(args.setting)
