from pyudev import Context
context = Context()
for device in context.list_devices(subsystem='input'):
    '{0} - {1}'.format(device.sys_name, device.device_type)
