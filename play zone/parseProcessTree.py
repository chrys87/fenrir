#!/bin/python
import os
import time
start = time.time()
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
#pids = ['5960']

tty = os.open('/dev/tty2', os.O_RDWR)
fg = str(os.tcgetpgrp(tty))
tty.close()
print(fg)
for pid in pids:
    try:
        currStat = str(open('/proc/' + pid + '/stat', 'rb').read())
        currStat = currStat.split(' ')      
        if int(currStat[4]) == 0:
            continue
        #print(currStat)
        #print(fg,int(currStat[4]))
        if fg == currStat[4]:
            print(currStat[1])
            #print( currStat )
            #print(currStat[0])
            major = os.major(int(currStat[6]))
            minor = os.minor(int(currStat[6]))
            ueventContent = open('/sys/dev/char/' + str(major) + ':' + str(minor) + '/uevent','r').read().split()
            #print(ueventContent)
            #print(int(currStat[4]),currStat[1])              
    except IOError: # proc has already terminated
        continue        

print(time.time()-start)      
  

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
