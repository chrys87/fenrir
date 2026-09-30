#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import MagicMock, patch

from fenrirscreenreader.utils.voice_utils import cycle_voice
from fenrirscreenreader.commands.commands.next_voice import command as NextVoiceCommand
from fenrirscreenreader.commands.commands.prev_voice import command as PrevVoiceCommand
from fenrirscreenreader.commands.commands.cycle_voice import command as CycleVoiceCommand
from fenrirscreenreader.core.speechDriver import speechDriver
from fenrirscreenreader.speechDriver.debugDriver import driver as DebugDriver
from fenrirscreenreader.speechDriver.dummyDriver import driver as DummyDriver
from fenrirscreenreader.speechDriver.speechdDriver import driver as SpeechdDriver
from fenrirscreenreader.speechDriver.espeakDriver import driver as EspeakDriver
from fenrirscreenreader.speechDriver.genericDriver import driver as GenericDriver
from fenrirscreenreader.speechDriver.pyttsxDriver import driver as PyttsxDriver
from fenrirscreenreader.core.outputManager import outputManager
from fenrirscreenreader.core.quickMenuManager import quickMenuManager


def create_mock_env(voices=None, current_voice="en-us", auto_save=False):
    """Helper to build a mock Fenrir runtime environment."""
    mock_settings_mgr = MagicMock()
    mock_settings_storage = {
        ("speech", "voice"): current_voice,
        ("speech", "autoSaveVoice"): "True" if auto_save else "False",
        ("menu", "quickMenu"): "speech#rate;speech#pitch;speech#volume;speech#voice",
    }

    def get_setting(section, key):
        return mock_settings_storage.get((section, key), "")

    def get_setting_as_bool(section, key):
        return mock_settings_storage.get((section, key), "False").upper() in ["TRUE", "1", "YES"]

    def set_setting(section, key, value):
        mock_settings_storage[(section, key)] = str(value)

    mock_settings_mgr.getSetting.side_effect = get_setting
    mock_settings_mgr.getSettingAsBool.side_effect = get_setting_as_bool
    mock_settings_mgr.setSetting.side_effect = set_setting
    mock_settings_mgr.getSettingsFile.return_value = "/etc/fenrir/settings/settings.conf"
    mock_settings_mgr.saveSettings = MagicMock()

    mock_speech_driver = MagicMock()
    if voices is not None:
        mock_speech_driver.getVoices.return_value = list(voices)
    else:
        mock_speech_driver.getVoices.return_value = []
    mock_speech_driver.setVoice = MagicMock()

    mock_output_mgr = MagicMock()
    mock_output_mgr.presentText = MagicMock()

    mock_debug = MagicMock()
    mock_debug.writeDebugOut = MagicMock()

    env = {
        "runtime": {
            "settingsManager": mock_settings_mgr,
            "speechDriver": mock_speech_driver,
            "outputManager": mock_output_mgr,
            "debug": mock_debug,
        },
        "settings": {},
        "general": {},
    }
    return env, mock_settings_storage


class TestVoiceCyclingLogic:
    def test_next_voice_advances_correctly(self):
        voices = ["voice_a", "voice_b", "voice_c"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_a")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "voice_b"
        env["runtime"]["speechDriver"].setVoice.assert_called_with("voice_b")
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_b", soundIcon="", interrupt=True)

        # Call next again
        cmd.run()
        assert storage[("speech", "voice")] == "voice_c"
        env["runtime"]["speechDriver"].setVoice.assert_called_with("voice_c")
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_c", soundIcon="", interrupt=True)

    def test_prev_voice_decrements_correctly(self):
        voices = ["voice_a", "voice_b", "voice_c"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_c")

        cmd = PrevVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "voice_b"
        env["runtime"]["speechDriver"].setVoice.assert_called_with("voice_b")
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_b", soundIcon="", interrupt=True)

        # Call prev again
        cmd.run()
        assert storage[("speech", "voice")] == "voice_a"
        env["runtime"]["speechDriver"].setVoice.assert_called_with("voice_a")
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_a", soundIcon="", interrupt=True)

    def test_cycle_voice_command_advances_forward(self):
        voices = ["voice_1", "voice_2", "voice_3"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_1")

        cmd = CycleVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "voice_2"
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_2", soundIcon="", interrupt=True)

    def test_boundary_wrapping_forward(self):
        voices = ["voice_a", "voice_b", "voice_c"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_c")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        # Should wrap from last back to first
        assert storage[("speech", "voice")] == "voice_a"
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_a", soundIcon="", interrupt=True)

    def test_boundary_wrapping_backward(self):
        voices = ["voice_a", "voice_b", "voice_c"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_a")

        cmd = PrevVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        # Should wrap from first back to last
        assert storage[("speech", "voice")] == "voice_c"
        env["runtime"]["outputManager"].presentText.assert_called_with("voice_c", soundIcon="", interrupt=True)

    def test_single_voice_list(self):
        voices = ["only_voice"]
        env, storage = create_mock_env(voices=voices, current_voice="only_voice")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()
        assert storage[("speech", "voice")] == "only_voice"
        env["runtime"]["outputManager"].presentText.assert_called_with("only_voice", soundIcon="", interrupt=True)

        cmd_prev = PrevVoiceCommand()
        cmd_prev.initialize(env)
        cmd_prev.run()
        assert storage[("speech", "voice")] == "only_voice"

    def test_unknown_or_empty_current_voice_defaults(self):
        voices = ["voice_x", "voice_y", "voice_z"]

        # Next voice when current is empty string
        env, storage = create_mock_env(voices=voices, current_voice="")
        cmd_next = NextVoiceCommand()
        cmd_next.initialize(env)
        cmd_next.run()
        assert storage[("speech", "voice")] == "voice_x"

        # Prev voice when current is non-matching
        env2, storage2 = create_mock_env(voices=voices, current_voice="nonexistent")
        cmd_prev = PrevVoiceCommand()
        cmd_prev.initialize(env2)
        cmd_prev.run()
        assert storage2[("speech", "voice")] == "voice_z"

    def test_case_insensitive_voice_matching(self):
        voices = ["en-us", "en-gb", "es-es"]
        env, storage = create_mock_env(voices=voices, current_voice="EN-US")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "en-gb"


class TestSpeechAnnouncementAndSaving:
    def test_speech_announcement_called_with_voice_name(self):
        voices = ["french", "german"]
        env, _ = create_mock_env(voices=voices, current_voice="french")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        env["runtime"]["outputManager"].presentText.assert_called_once_with("german", soundIcon="", interrupt=True)

    def test_save_setting_on_demand(self):
        voices = ["voice_1", "voice_2"]
        env, _ = create_mock_env(voices=voices, current_voice="voice_1", auto_save=False)

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run(save=True)

        env["runtime"]["settingsManager"].saveSettings.assert_called_once_with("/etc/fenrir/settings/settings.conf")

    def test_auto_save_voice_setting(self):
        voices = ["voice_1", "voice_2"]
        env, _ = create_mock_env(voices=voices, current_voice="voice_1", auto_save=True)

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run(save=False)

        env["runtime"]["settingsManager"].saveSettings.assert_called_once_with("/etc/fenrir/settings/settings.conf")

    def test_no_save_when_disabled(self):
        voices = ["voice_1", "voice_2"]
        env, _ = create_mock_env(voices=voices, current_voice="voice_1", auto_save=False)

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run(save=False)

        env["runtime"]["settingsManager"].saveSettings.assert_not_called()


class TestFallbackBehavior:
    def test_fallback_when_voices_list_is_empty(self):
        env, storage = create_mock_env(voices=[], current_voice="default_voice")

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        # Setting must remain unchanged
        assert storage[("speech", "voice")] == "default_voice"
        env["runtime"]["outputManager"].presentText.assert_called_with("No voices available", soundIcon="", interrupt=True)

    def test_fallback_when_speech_driver_is_none(self):
        env, storage = create_mock_env(voices=None, current_voice="default_voice")
        env["runtime"]["speechDriver"] = None

        cmd = NextVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "default_voice"
        env["runtime"]["outputManager"].presentText.assert_called_with("No voices available", soundIcon="", interrupt=True)

    def test_fallback_when_get_voices_raises_exception(self):
        env, storage = create_mock_env(voices=None, current_voice="default_voice")
        env["runtime"]["speechDriver"].getVoices.side_effect = RuntimeError("Driver crashed")

        cmd = PrevVoiceCommand()
        cmd.initialize(env)
        cmd.run()

        assert storage[("speech", "voice")] == "default_voice"
        env["runtime"]["outputManager"].presentText.assert_called_with("No voices available", soundIcon="", interrupt=True)


class TestQuickMenuIntegration:
    def test_quick_menu_voice_navigation_and_cycling(self):
        voices = ["voice_1", "voice_2", "voice_3"]
        env, storage = create_mock_env(voices=voices, current_voice="voice_1")

        qm = quickMenuManager()
        qm.initialize(env)

        # Quick menu entries: rate, pitch, volume, voice
        # Navigate to voice entry (index 3)
        assert qm.nextEntry()  # pitch
        assert qm.nextEntry()  # volume
        assert qm.nextEntry()  # voice
        assert "voice" in qm.getCurrentEntry()

        # Advance value on voice
        success = qm.nextValue()
        assert success is True
        assert storage[("speech", "voice")] == "voice_2"
        assert qm.getCurrentValue() == "voice_2"

        # Decrement value on voice
        success = qm.prevValue()
        assert success is True
        assert storage[("speech", "voice")] == "voice_1"
        assert qm.getCurrentValue() == "voice_1"

    def test_quick_menu_voice_empty_fallback(self):
        env, storage = create_mock_env(voices=[], current_voice="voice_1")

        qm = quickMenuManager()
        qm.initialize(env)

        qm.position = 3  # Position at voice
        success = qm.nextValue()
        assert success is False
        env["runtime"]["outputManager"].presentText.assert_called_with("No voices available", soundIcon="", interrupt=True)


class TestDriversGetVoices:
    def test_base_speech_driver(self):
        d = speechDriver()
        assert d.getVoices() == []
        d._isInitialized = True
        d.setVoice("test_voice")
        assert d.getVoice() == "test_voice"

    def test_debug_driver(self):
        d = DebugDriver()
        voices = d.getVoices()
        assert isinstance(voices, list)
        assert len(voices) > 0
        assert "en-us" in voices

    def test_dummy_driver(self):
        d = DummyDriver()
        assert d.getVoices() == []

    def test_output_manager_delegation(self):
        env, _ = create_mock_env(voices=["voice_1", "voice_2"])
        om = outputManager()
        om.env = env
        assert om.getVoices() == ["voice_1", "voice_2"]

        om.setVoice("voice_2")
        env["runtime"]["speechDriver"].setVoice.assert_called_with("voice_2")

    def test_speechd_driver_parsing(self):
        d = SpeechdDriver()
        d.env = {"runtime": {"debug": MagicMock()}}
        d._isInitialized = True
        mock_sd = MagicMock()
        mock_sd.list_synthesis_voices.return_value = [
            ("voice1", "en", "none"),
            ("voice2", "fr", "none"),
        ]
        d._sd = mock_sd

        voices = d.getVoices()
        assert voices == ["voice1", "voice2"]

    def test_pyttsx_driver_parsing(self):
        d = PyttsxDriver()
        d.env = {"runtime": {"debug": MagicMock()}}
        d._isInitialized = True
        mock_engine = MagicMock()
        v1 = MagicMock()
        v1.id = "id1"
        v2 = MagicMock()
        v2.id = "id2"
        mock_engine.getProperty.return_value = [v1, v2]
        d._engine = mock_engine

        voices = d.getVoices()
        assert voices == ["id1", "id2"]

    def test_generic_driver_cli_parsing(self):
        d = GenericDriver()
        cli_output = """Pty Language Age/Gender VoiceName File Other Languages
 5  en-us          M  en-us                americas/en-us
 2  en-gb          M  english              europe/en-gb
 5  de             M  german               europe/de
"""
        with patch("subprocess.run") as mock_run:
            mock_res = MagicMock()
            mock_res.returncode = 0
            mock_res.stdout = cli_output
            mock_run.return_value = mock_res

            voices = d.getVoices()
            assert "en-us" in voices
            assert "en-gb" in voices
            assert "de" in voices

    def test_espeak_driver_cli_fallback(self):
        d = EspeakDriver()
        d.env = {"runtime": {"debug": MagicMock()}}
        d._isInitialized = True
        d._es = MagicMock()
        d._es.list_voices.side_effect = AttributeError("no list_voices")

        cli_output = """Pty Language Age/Gender VoiceName File Other Languages
 5  es             M  spanish              europe/es
 5  fr             M  french               europe/fr
"""
        with patch("subprocess.run") as mock_run:
            mock_res = MagicMock()
            mock_res.returncode = 0
            mock_res.stdout = cli_output
            mock_run.return_value = mock_res

            voices = d.getVoices()
            assert "es" in voices
            assert "fr" in voices


class TestCommandAndConfigRegistration:
    def test_command_manager_loads_voice_commands(self):
        import os
        from fenrirscreenreader.core.commandManager import commandManager
        from fenrirscreenreader.core.environment import environment

        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cmd_path = os.path.join(repo_root, "src", "fenrirscreenreader", "commands") + "/"

        cm = commandManager()
        env = environment.copy()
        env["commands"] = {}
        env["commandsIgnore"] = {}
        env["runtime"] = {"commandManager": cm, "debug": MagicMock()}
        cm.env = env
        cm.loadCommands("commands", cmd_path)

        assert "NEXT_VOICE" in env["commands"]["commands"]
        assert "PREV_VOICE" in env["commands"]["commands"]
        assert "CYCLE_VOICE" in env["commands"]["commands"]
        assert len(env["commands"]["commands"]["NEXT_VOICE"].getDescription()) > 0
        assert len(env["commands"]["commands"]["PREV_VOICE"].getDescription()) > 0
        assert len(env["commands"]["commands"]["CYCLE_VOICE"].getDescription()) > 0

    @pytest.mark.parametrize("conf_name", [
        "desktop.conf",
        "laptop.conf",
        "nvda-desktop.conf",
        "nvda-laptop.conf",
        "speakup.conf",
    ])
    def test_keyboard_layouts_bind_voice_commands(self, conf_name):
        import os
        from fenrirscreenreader.core.inputManager import inputManager
        from fenrirscreenreader.core.environment import environment

        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        conf_path = os.path.join(repo_root, "config", "keyboard", conf_name)

        im = inputManager()
        env = environment.copy()
        env["bindings"] = {}
        env["rawBindings"] = {}
        env["runtime"] = {"inputManager": im, "debug": MagicMock()}
        im.env = env
        im.loadShortcuts(conf_path)

        assert "NEXT_VOICE" in env["bindings"].values()
        assert "PREV_VOICE" in env["bindings"].values()

    def test_quick_menu_configuration(self):
        from fenrirscreenreader.core.settingsData import settingsData
        assert "speech#voice" in settingsData["menu"]["quickMenu"]

