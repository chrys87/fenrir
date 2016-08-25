#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        try:
            #Need to load time string from config file.
        except Exception as e:
            # Sane default
            timeString = '%H:%M;%P'

        timeString = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%P')
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass
