#!/bin/python
iDevices = {}
def updateInputDevices():
    deviceFileList = evdev.list_devices()
    mode = 'ALL'
    iDevicesFiles = []
    for device in iDevices:
        iDevicesFiles.append(iDevices[device].fn)
    print(len(iDevicesFiles),len(deviceFileList))
    if len(iDevicesFiles) == len(deviceFileList):
        return
    for deviceFile in deviceFileList:
        try:
            if deviceFile in iDevicesFiles:
                print('skip')
                continue        
            open(deviceFile)
            # 3 pos absolute
            # 2 pos relative
            # 1 Keys
            currDevice = evdev.InputDevice(deviceFile)
            cap = currDevice.capabilities()
            if mode in ['ALL','NOMICE']:
                if 1 in cap:
                    if 116 in cap[1] and len(cap[1]) < 5:
                        print('power')
                        continue
                    if mode == 'ALL':
                        iDevices[currDevice.fd] = currDevice
                        print('Device added:' + iDevices[currDevice.fd].name)
                    elif mode == 'NOMICE':
                        if not ((2 in cap) or (3 in cap)):
                            iDevices[currDevice.fd] = currDevice
                            print('Device added:' + iDevices[currDevice.fd].name)
            elif currDevice.name.upper() in mode.split(','):
                iDevices[currDevice.fd] = currDevice
                print('Device added:' + iDevices[currDevice.fd].name)
        except Exception as e:
            print("Skip Inputdevice : " + deviceFile +' ' + str(e))                     
