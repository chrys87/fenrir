#!/bin/python
#https://python-packaging.readthedocs.io/en/latest/minimal.html
import os, glob
from setuptools import find_packages
from setuptools import setup
fenrirVersion = '1.5'

data_files = []
directories = glob.glob('config/*/*')
for directory in directories:
    files = glob.glob(directory+'/*')
    destDir = '/etc/fenrir'
    if directory == 'config/punctuation':
        destDir = '/etc/fenrir/punctuation'
    elif directory == 'config/keyboard':
        destDir = '/etc/fenrir/keyboard'
    if directory == 'config/settings':
        destDir = '/etc/fenrir/settings'
    elif directory == 'config/scripts':
        destDir = '/usr/share/fenrir/scripts' 
    elif 'config/sound' in directory:
        destDir = '/usr/share/sounds/fenrir'  
    data_files.append((destDir, files))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # Application name:
    name="fenrir",
    # Version number (initial):
    version=fenrirVersion,
    # description
    description="An TTY Screen Reader For Linux.",
    long_description=read('README.md'),
    keywords=['screenreader', 'a11y', 'accessibility', 'terminal', 'TTY', 'console'],        
    license="License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    url="https://github.com/chrys87/fenrir/",
    download_url = 'https://github.com/chrys87/fenrir/archive/' + fenrirVersion + '.tar.gz',	
    classifiers=[
        "Programming Language :: Python",        
        "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Environment :: Console",        
    ],
    
    # Application author details:
    author="Chrys, storm_dragon, Jeremiah and others",
    author_email="chrysg@linux-a11y.org",

    # Packages
    packages=find_packages('src/fenrir'),
    package_dir={'': 'src/fenrir'},
    scripts=['src/fenrir/fenrir','src/fenrir/fenrir-daemon'],

    # Include additional files into the package
    include_package_data=True,
    zip_safe=False,

    data_files=data_files,
    
    # Dependent packages (distributions)
    install_requires=[
        "evdev",
        "sox",
        "dbus-python",
        "pyenchant",
        "pyudev",
        "setuptools",
    ],
    
)

