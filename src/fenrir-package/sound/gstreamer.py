import gi
from gi.repository import GLib

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)

class sound:
    """Plays Icons and Tones."""

    def __init__(self):
        self._initialized = False
        self._source = None
        self._sink = None
        if not _gstreamerAvailable:
            return
        self.init()

    def _onPlayerMessage(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self._player.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._player.set_state(Gst.State.NULL)
            error, info = message.parse_error()

    def _onPipelineMessage(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self._pipeline.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self._pipeline.set_state(Gst.State.NULL)
            error, info = message.parse_error()

    def _onTimeout(self, element):
        element.set_state(Gst.State.NULL)
        return False

    def playSoundFile(self, fileName, interrupt=True):
        if interrupt:
            self.stop()
        self._player.set_property('uri', 'file://%s' % fileName)
        self._player.set_state(Gst.State.PLAYING)

    def playFrequence(self, frequence, duration, adjustVolume, interrupt=True):
        if interrupt:
            self.stop()
        self._source.set_property('volume', tone.volume)
        self._source.set_property('freq', tone.frequency)
        self._source.set_property('wave', tone.wave)
        self._pipeline.set_state(Gst.State.PLAYING)
        duration = int(1000 * tone.duration)
        GLib.timeout_add(duration, self._onTimeout, self._pipeline)

    def init(self):
        """(Re)Initializes the Player."""
        if self._initialized:
            return
        if not _gstreamerAvailable:
            return

        self._player = Gst.ElementFactory.make('playbin', 'player')
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._onPlayerMessage)

        self._pipeline = Gst.Pipeline(name='fenrir-pipeline')
        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._onPipelineMessage)

        self._source = Gst.ElementFactory.make('audiotestsrc', 'src')
        self._sink = Gst.ElementFactory.make('autoaudiosink', 'output')
        self._pipeline.add(self._source)
        self._pipeline.add(self._sink)
        self._source.link(self._sink)

        self._initialized = True

    def stop(self, element=None):
        if not _gstreamerAvailable:
            return
        if element:
            element.set_state(Gst.State.NULL)
            return
        self._player.set_state(Gst.State.NULL)
        self._pipeline.set_state(Gst.State.NULL)

    def shutdown(self):
        global _gstreamerAvailable
        if not _gstreamerAvailable:
            return
        self.stop()
        self._initialized = False
        _gstreamerAvailable = False


