#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

try:
    _
except NameError:
    _ = lambda s: s

def cycle_voice(env, direction=1, save=False, announce=True):
    speech_driver = env['runtime'].get('speechDriver', None)
    voices = []
    if speech_driver and hasattr(speech_driver, 'getVoices'):
        try:
            driver_voices = speech_driver.getVoices()
            if driver_voices:
                voices = list(driver_voices)
        except Exception as e:
            env['runtime']['debug'].writeDebugOut('getVoices error:' + str(e), debug.debugLevel.ERROR)

    if not voices:
        env['runtime']['outputManager'].presentText(_('No voices available'), soundIcon='', interrupt=True)
        return False

    current_voice = env['runtime']['settingsManager'].getSetting('speech', 'voice')
    curr_idx = -1
    for idx, v in enumerate(voices):
        if v == current_voice:
            curr_idx = idx
            break
    if curr_idx == -1:
        for idx, v in enumerate(voices):
            if str(v).lower() == str(current_voice).lower():
                curr_idx = idx
                break

    if curr_idx == -1:
        if direction > 0:
            new_idx = 0
        else:
            new_idx = len(voices) - 1
    else:
        new_idx = (curr_idx + direction) % len(voices)

    new_voice = str(voices[new_idx])
    env['runtime']['settingsManager'].setSetting('speech', 'voice', new_voice)
    try:
        if speech_driver and hasattr(speech_driver, 'setVoice'):
            speech_driver.setVoice(new_voice)
    except Exception as e:
        env['runtime']['debug'].writeDebugOut('setVoice error:' + str(e), debug.debugLevel.ERROR)

    should_save = save
    try:
        if env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoSaveVoice'):
            should_save = True
    except Exception:
        pass

    if should_save:
        try:
            settings_file = env['runtime']['settingsManager'].getSettingsFile()
            if settings_file:
                env['runtime']['settingsManager'].saveSettings(settings_file)
        except Exception as e:
            env['runtime']['debug'].writeDebugOut('saveSettings error:' + str(e), debug.debugLevel.ERROR)

    if announce:
        env['runtime']['outputManager'].presentText(new_voice, soundIcon='', interrupt=True)

    return True
