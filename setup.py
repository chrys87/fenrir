#!/bin/python
#https://python-packaging.readthedocs.io/en/latest/minimal.html
import os, glob
from setuptools import find_packages
from setuptools import setup
fenrirVersion = '1.5'
packageVersion = 'post4'

data_files = []
directories = glob.glob('config/*')
for directory in directories:
    files = glob.glob(directory+'/*') 
    destDir = ''
    if 'config/punctuation' in directory :
        destDir = '/etc/fenrir/punctuation'
    elif 'config/keyboard' in directory:
        destDir = '/etc/fenrir/keyboard'
    elif 'config/settings' in directory:
        destDir = '/etc/fenrir/settings'
    elif 'config/scripts' in directory:
        destDir = '/usr/share/fenrir/scripts' 
    if destDir != '':
        data_files.append((destDir, files))

files = glob.glob('config/sound/default-wav/*')         
destDir = '/usr/share/sounds/fenrir/default-wav'
data_files.append((destDir, files))        
files = glob.glob('config/sound/default/*')                 
destDir = '/usr/share/sounds/fenrir/default'            
data_files.append((destDir, files))
files = glob.glob('config/sound//template/*')                 
destDir = '/usr/share/sounds/fenrir/template'
data_files.append((destDir, files))
files = glob.glob('tools/*') 
data_files.append(('/usr/share/fenrir/tools', files))
data_files.append(('/usr/lib/systemd/system', ['autostart/systemd/fenrir.service']))
data_files.append(('/usr/share/man/man1', ['docu/fenrir.1']))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # Application name:
    name="fenrir-screenreader",
    # Version number:
    version=fenrirVersion + '.' + packageVersion,
    # description
    description="A TTY Screen Reader for Linux.",
    long_description=read('README.md'),
    keywords=['screenreader', 'a11y', 'accessibility', 'terminal', 'TTY', 'console'],        
    license="License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    url="https://github.com/chrys87/fenrir/",
    download_url = 'https://github.com/chrys87/fenrir/archive/' + fenrirVersion + '.tar.gz',	
    classifiers=[
        "Programming Language :: Python",        
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",        
        "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Environment :: Console",        
    ],
    
    # Application author details:
    author="Chrys, Storm_dragon, Jeremiah and others",
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
        "daemonize",
        "dbus-python",
        "pyenchant",
        "pyudev",
        "setuptools",
    ],
    
)
print('')
print('To have Fenrir start at boot:')
print('sudo systemctl enable fenrir')
print('Pulseaudio users may want to run:')
print('/usr/share/fenrir/tools/configure_pulse.sh')
print('once as their user account and once as root to configure Pulseaudio.')
print('Please install the following packages manually:')
print('- Speech-dispatcher: for the default speech driver')
print('- Espeak: as basic TTS engine')
print('- BrlTTY: for Braille')
print('- sox: is a player for the generic sound driver')
