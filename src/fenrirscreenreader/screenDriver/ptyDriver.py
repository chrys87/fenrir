#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
from fenrirscreenreader.core.screenDriver import screenDriver
from fenrirscreenreader.utils import screen_utils
import os, struct, sys, pty, tty, termios, shlex, signal, select, pyte, time, fcntl ,getpass
from multiprocessing.sharedctypes import Value
from ctypes import c_int


class Terminal:
    def __init__(self, columns, lines, p_in):
        self.text = ''
        self.attributes = None
        self.screen = pyte.HistoryScreen(columns, lines)
        self.screen.set_mode(pyte.modes.LNM)
        self.screen.write_process_input = \
            lambda data: p_in.write(data.encode())
        self.stream = pyte.ByteStream()
        self.stream.attach(self.screen)
    def feed(self, data):
        self.stream.feed(data)
            
    def updateAttributes(self, initialize = False):
        buffer = self.screen.buffer    
        lines = None
        if not initialize:
            lines = self.screen.dirty
        else:
            lines = range(self.screen.lines)
            self.attributes = [[list(attribute[1:]) + [False, 'default', 'default'] for attribute in line.values()] for line in buffer.values()]            
            
        for y in lines:
            try:
                t = self.attributes[y]
            except:
                self.attributes.append([])

            self.attributes[y] = [list(attribute[1:]) + [False, 'default', 'default'] for attribute in (buffer[y].values())]
            if len(self.attributes[y]) < self.screen.columns:
                diff = self.screen.columns - len(self.attributes[y])
                self.attributes[y] += [['default', 'default', False, False, False, False, False, False, 'default', 'default']]   * diff

    def resize(self, lines, columns):
        self.screen.resize(lines, columns)
        self.setCursor()
        self.updateAttributes(True)
    def setCursor(self, x = -1, y = -1):
        xPos = x
        yPos = y
        if xPos == -1:
            xPos = self.screen.cursor.x
        if yPos == -1:
            yPos = self.screen.cursor.y
        self.screen.cursor.x = min(self.screen.cursor.x, self.screen.columns - 1)
        self.screen.cursor.y = min(self.screen.cursor.y, self.screen.lines - 1)            
    def GetScreenContent(self):
        cursor = self.screen.cursor
        self.text = '\n'.join(self.screen.display)
        self.updateAttributes(self.attributes == None)
        self.screen.dirty.clear()            
        return {"cursor": (cursor.x, cursor.y),
            'lines': self.screen.lines,
            'columns': self.screen.columns,
            "text": self.text, 
            'attributes': self.attributes.copy(),
            'screen': 'pty',        
            'screenUpdateTime': time.time(),
        }.copy()

class driver(screenDriver):
    def __init__(self):
        screenDriver.__init__(self)
        self.signalPipe = os.pipe()
        self.p_out = Value(c_int, 0)
        self.p_pid = Value(c_int, 0)
        signal.signal(signal.SIGWINCH, self.handleSigwinch)
    def initialize(self, environment):
        self.env = environment
        self.command = self.env['runtime']['settingsManager'].getSetting('general','shell')
        self.shortcutType = self.env['runtime']['inputManager'].getShortcutType()
        param = [sys.stdin.fileno(), sys.stdout.fileno(), self.signalPipe, self.p_out, self.p_pid]
        #param[0] = sys.stdin
        #param[1] = sys.stdout
        #param[2] = self.signalPipe
        #param[3] = self.p_out
        #param[4] = self.p_pid
        self.env['runtime']['processManager'].addCustomEventThread(self.terminalEmulation, pargs = param, multiprocess = False)
    def getCurrScreen(self):
        self.env['screen']['oldTTY'] = 'pty'
        self.env['screen']['newTTY'] = 'pty'
 
    def injectTextToScreen(self, msgBytes, screen = None):
        #if not screen:
        #    try:
        #        screen = os.fdopen(int(self.p_out.value), 'w+b', 0)
        #    except Exception as e:
        #        print(e)
        #    if screen < 1:
        #        return
        print(self.p_out.value,self.p_out)
        os.write(self.p_out.value, 'test')
        return
        try:
            screen = os.fdopen(self.p_out.value, "w+b", 0)
        except Exception as e:
            print(e)
        
        if isinstance(msgBytes, str):
            msgBytes = bytes(msgBytes, 'UTF-8')
        try:
            screen.write(msgBytes)
        except Exception as e:
            print(int(self.p_out.value), msgBytes,e)

    def getSessionInformation(self):
        self.env['screen']['autoIgnoreScreens'] = []
        self.env['general']['prevUser'] = getpass.getuser()
        self.env['general']['currUser'] = getpass.getuser()
    def readAll(self, fd, timeout = 9999999, interruptFd = None, len = 2048):
        bytes = b'' 
        fdList = []
        fdList += [fd]        
        if interruptFd:
            fdList += [interruptFd]
        starttime = time.time()
        while True:
            # respect timeout but wait a little bit of time to see if something more is here
            if (time.time() - starttime) >= timeout:
                break            
            r = screen_utils.hasMoreWhat(fdList,0)
            hasmore = fd in r
            if not hasmore:
                break
            # exit on interrupt available
            if interruptFd in r:
                break
            data = os.read(fd, len)
            if data == b'':
                raise EOFError
            bytes += data
        return bytes      
    def openTerminal(self, columns, lines, command):
        p_pid, master_fd = pty.fork()
        if p_pid == 0:  # Child.
            argv = shlex.split(command)
            env = os.environ.copy()
            #values are VT100,xterm-256color,linux
            env["TERM"] = 'linux'
            os.execvpe(argv[0], argv, env)
        # File-like object for I/O with the child process aka command.
        p_out = os.fdopen(master_fd, "w+b", 0)
        return Terminal(columns, lines, p_out), p_pid, p_out.fileno()
    def resizeTerminal(self,fd):
        s = struct.pack('HHHH', 0, 0, 0, 0)
        s = fcntl.ioctl(0, termios.TIOCGWINSZ, s)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
        lines, columns, _, _ = struct.unpack('hhhh', s)
        return lines, columns
    def getTerminalSize(self, fd):
        s = struct.pack('HHHH', 0, 0, 0, 0)
        lines, columns, _, _ = struct.unpack('HHHH', fcntl.ioctl(fd, termios.TIOCGWINSZ, s))
        return lines, columns
    def handleSigwinch(self, *args):
        os.write(self.signalPipe[1], b'w')        
    def terminalEmulation(self,active , eventQueue, param = None):
        try:
            #stdin = param[0]
            stdin = os.fdopen(param[0])
            stdout = os.fdopen(param[1])
            signalPipe = param[2]
            p_outFd = param[3]
            p_pid = param[4]
            old_attr = termios.tcgetattr(stdin)    
            tty.setraw(0)
            lines, columns = self.getTerminalSize(0)
            if self.command == '':
                self.command = screen_utils.getShell()
            terminal, p_pid.value, fd = self.openTerminal(columns, lines, self.command)
            p_outFd.value = os.dup(fd)
            p_out = fd
            
            #p_out = os.fdopen(p_outFd.value, "r+b", 0)
            lines, columns = self.resizeTerminal(p_out)
            terminal.resize(lines, columns)            
            fdList = [stdin, p_out, signalPipe[0]]
            while active.value:
                r, _, _ = select.select(fdList, [], [], 1)
                # none
                if r == []:
                    continue
                # signals
                if signalPipe[0] in r:
                    os.read(signalPipe[0], 1)
                    lines, columns = self.resizeTerminal(p_out)
                    terminal.resize(lines, columns)   
                # input
                if stdin in r:
                    try:
                        msgBytes = self.readAll(stdin.fileno())
                    except (EOFError, OSError):
                        active.value = False                    
                        break                  
                    if self.shortcutType == 'KEY':
                        try:
                            self.injectTextToScreen(msgBytes)
                        except:
                            active.value = False                    
                            break
                    else:    
                        eventQueue.put({"Type":fenrirEventType.ByteInput,
                            "Data":msgBytes })                     
                # output
                if p_out in r:
                    try:
                        msgBytes = self.readAll(p_out, timeout=0.001, interruptFd=stdin)
                    except (EOFError, OSError):
                        active.value = False
                        break    
                    terminal.feed(msgBytes)                                
                    os.write(stdout.fileno(), msgBytes)
                    eventQueue.put({"Type":fenrirEventType.ScreenUpdate,
                        "Data":screen_utils.createScreenEventData(terminal.GetScreenContent())
                    })
        except Exception as e:  # Process died?
            print(e)
            active.value = False
        finally:
            os.kill(p_pid, signal.SIGTERM)
            p_out.close()    
            termios.tcsetattr(stdin, termios.TCSADRAIN, old_attr)
            eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
            sys.exit(0)
         
    def getCurrApplication(self):
        pass
