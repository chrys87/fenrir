#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, struct, sys, pty, tty, termios, shlex, signal, select, pyte, time, fcntl ,getpass
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
from fenrirscreenreader.core.screenDriver import screenDriver
from fenrirscreenreader.utils import screen_utils

class Terminal:
    def __init__(self, columns, lines, p_in):
        self.screen = pyte.HistoryScreen(columns, lines)
        self.screen.set_mode(pyte.modes.LNM)
        self.screen.write_process_input = \
            lambda data: p_in.write(data.encode())
        self.stream = pyte.ByteStream()
        self.stream.attach(self.screen)
    def feed(self, data):
        self.stream.feed(data)
    def resize(self, lines, columns):
        self.screen.resize(lines, columns)
        self.setCursor()
    def setCursor(self, x = -1, y = -1):
        xPos = x
        yPos = y
        if xPos == -1:
            xPos = self.screen.cursor.x
        if yPos == -1:
            yPos = self.screen.cursor.y
        self.screen.cursor.x = min(self.screen.cursor.x, self.screen.columns - 1)
        self.screen.cursor.y = min(self.screen.cursor.y, self.screen.lines - 1)            
    def dump(self):
        cursor = self.screen.cursor
        allAttributes = []
        text = '\n'.join(self.screen.display)
        for y in range(self.screen.lines):
            line = self.screen.buffer[y]
            attributes = [(char.reverse, char.fg, char.bg, char.bold, char.italics, char.underscore, char.strikethrough)
                    for char in (line[x] for x in range(self.screen.columns))]            
            allAttributes.append((attributes))
        self.screen.dirty.clear()
        return {"cursor": (cursor.x, cursor.y),
            'lines': self.screen.lines,
            'columns': self.screen.columns,
            "text": text, 
            'attributes': allAttributes,
            'screen': '1'            
        }.copy()

class driver(screenDriver):
    def __init__(self):
        screenDriver.__init__(self)
        self.bgColorNames = {0: _('black'), 1: _('blue'), 2: _('green'), 3: _('cyan'), 4: _('red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('white')}
        self.fgColorNames = {0: _('Black'), 1: _('Blue'), 2: _('Green'), 3: _('Cyan'), 4: _('Red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('Light gray'), 8: _('Dark gray'), 9: _('Light blue'), 10: ('Light green'), 11: _('Light cyan'), 12: _('Light red'), 13: _('Light magenta'), 14: _('Light yellow'), 15: _('White')}
        self.signalPipe = os.pipe()
        self.p_out = None
        self.
        signal.signal(signal.SIGWINCH, self.handleSigwinch)
    def initialize(self, environment):
        self.env = environment
        self.ShortcutType = self.env['runtime']['inputManager'].getShortcutType()
        self.command = self.env['runtime']['settingsManager'].getSetting('general','shell')
        self.env['runtime']['processManager'].addCustomEventThread(self.terminalEmulation)
    def getCurrScreen(self):
        self.env['screen']['oldTTY'] = '1'
        self.env['screen']['newTTY'] = '1'
 
    def injectTextToScreen(self, msgBytes, screen = None):
        if not screen:
            screen = self.p_out.fileno()
        if isinstance(msgBytes, str):
            msgBytes = bytes(msgBytes, 'UTF-8')
        os.write(screen, msgBytes)
        #print(str(msgBytes))

    def getSessionInformation(self):
        self.env['screen']['autoIgnoreScreens'] = []
        self.env['general']['prevUser'] = getpass.getuser()
        self.env['general']['currUser'] = getpass.getuser()
    def readAll(self,fd, timeout = 9999999):
        bytes = os.read(fd, 65536)
        if bytes == b'':
            raise EOFError
        starttime = time.time()
        # respect timeout but wait a little bit of time to see if something more is here
        while screen_utils.hasMore(fd,0.0000001) and (time.time() - starttime) >= timeout:
            data = os.read(fd, 65536)
            if data == b'':
                raise EOFError
            bytes += data
        return bytes      
    def openTerminal(self, columns, lines, command):
        p_pid, master_fd = pty.fork()
        if p_pid == 0:  # Child.
            argv = shlex.split(command)
            env = os.environ.copy()
            env["TERM"] = 'vt100'
            os.execvpe(argv[0], argv, env)
        # File-like object for I/O with the child process aka command.
        p_out = os.fdopen(master_fd, "w+b", 0)
        return Terminal(columns, lines, p_out), p_pid, p_out
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
    def terminalEmulation(self,active , eventQueue):
        try:
            old_attr = termios.tcgetattr(sys.stdin)    
            tty.setraw(0)
            lines, columns = self.getTerminalSize(0)
            if self.command == '':
                self.command = screen_utils.getShell()
            terminal, p_pid, self.p_out = self.openTerminal(columns, lines, self.command)
            lines, columns = self.resizeTerminal(self.p_out)
            terminal.resize(lines, columns)            
            while active.value:
                r, _, _ = select.select([sys.stdin, self.p_out, self.signalPipe[0]],[],[],1)
                # none
                if r == []:
                    continue
                # signals
                if self.signalPipe[0] in r:
                    os.read(self.signalPipe[0], 1)
                    lines, columns = self.resizeTerminal(self.p_out)
                    terminal.resize(lines, columns)   
                # input
                if sys.stdin in r:
                    try:
                        msgBytes = self.readAll(sys.stdin.fileno())
                    except (EOFError, OSError):
                        active.value = False                    
                        break                  
                    if self.ShortcutType == 'KEY':
                        try:
                            self.injectTextToScreen(msgBytes)
                        except:
                            active.value = False                    
                            break
                    else:    
                        eventQueue.put({"Type":fenrirEventType.ByteInput,
                            "Data":msgBytes })                     
                # output
                if self.p_out in r:
                    try:
                        msgBytes = self.readAll(self.p_out.fileno(), timeout=0.01)
                    except (EOFError, OSError):
                        active.value = False
                        break    
                    terminal.feed(msgBytes)                                
                    os.write(sys.stdout.fileno(), msgBytes)
                    eventQueue.put({"Type":fenrirEventType.ScreenUpdate,
                        "Data":screen_utils.createScreenEventData(terminal.dump())
                    })
        except Exception as e:  # Process died?
            print(e)
            active.value = False
        finally:
            os.kill(p_pid, signal.SIGTERM)
            self.p_out.close()    
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
            eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None}) 
            sys.exit(0)

    def getFenrirBGColor(self, attribute):
        try:
            return self.bgColorNames[attribute[2]]
        except Exception as e:
            print(e)
            return ''
    def getFenrirFGColor(self, attribute):
        try:
            return self.fgColorNames[attribute[1]]
        except Exception as e:
            print(e)        
            return ''
    def getFenrirUnderline(self, attribute):
        if attribute[5] == 1:
            return _('underlined')
        return ''    
    def getFenrirBold(self, attribute):
        if attribute[4] == 1:
            return _('bold')    
        return ''    
    def getFenrirBlink(self, attribute):
        if attribute[3] == 1:
            return _('blink')    
        return ''    
    def getFenrirFont(self, attribute):
        return _('Default')
    def getFenrirFontSize(self, attribute):
        return _('Default')              
    def getCurrApplication(self):
        pass
