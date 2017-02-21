#!/bin/python
import os
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    try:
        currStat = open(os.path.join('/proc', pid, 'stat'), 'rb').read()
        currStat = currStat.split()
        if b'agetty' in currStat[1]:
            print( currStat )
            print(currStat[0])
            os.major(int(currStat[6]))
            os.minor(int(currStat[6]))
    except IOError: # proc has already terminated
        continue        
        
'''
Table 1-4: Contents of the stat files (as of 2.6.30-rc7)
..............................................................................
 Field          Content
  pid           process id
  tcomm         filename of the executable
  state         state (R is running, S is sleeping, D is sleeping in an
                uninterruptible wait, Z is zombie, T is traced or stopped)
  ppid          process id of the parent process
  pgrp          pgrp of the process
  sid           session id
  tty_nr        tty the process uses
  tty_pgrp      pgrp of the tty
  flags         task flags
  min_flt       number of minor faults
  cmin_flt      number of minor faults with child's
  maj_flt       number of major faults
  cmaj_flt      number of major faults with child's
'''        
