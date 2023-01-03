import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import Gdk
from gi.repository import GLib

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super(AppWindow, self).__init__(application=app)
        self.init_ui()

    def init_ui(self):
        self.set_title('Test Player')

        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
        hbox.set_margin_start(5)
        hbox.set_margin_top(5)
        hbox.set_margin_bottom(5)
        hbox.spacing=5,
        hbox.hexpand=False,
        hbox.vexpand=False    
        
        self.button_play_pause = Gtk.Button(
            hexpand=False,
            vexpand=False
            )
        
        self.button_play_pause.set_icon_name("media-playback-start")
        
        self.button_play_pause.connect(
            "clicked", 
            self.play_pause_clicked
            )
        
        self.button_stop = Gtk.Button(
            hexpand=False,
            vexpand=False
            )
            
        self.button_stop.set_icon_name("media-playback-stop")

        self.button_stop.connect(
            "clicked", 
            self.stop_clicked
            )
        
        self.scale = Gtk.Scale()
        #self.scale.set_digits(0)  # Number of decimal places to use
        self.scale.set_range(0, 1000)
        self.scale.set_draw_value(False)  # Don't display current value
        self.scale.set_value(0)  # Sets the starting value/position as 0
        self.scale.set_hexpand(True)
        self.scale_handler_id = self.scale.connect(
            'value-changed', 
            self.scale_changed
            )
        
        self.label = Gtk.Label.new('00:00 / 00:00')
        self.label.margin = 5
        
        hbox.append(self.button_play_pause)
        hbox.append(self.button_stop)
        hbox.append(self.scale)
        hbox.append(self.label)
             
        self.set_title('Scale Slider')
        self.set_default_size(450, 50)
        self.set_child(hbox)
        
        Gst.init(None)
        self.player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        audio_sink = Gst.ElementFactory.make("alsasink", "audio_sink")
        #sink_pre.set_property("device", soundcard)
        self.player.set_property("video-sink", fakesink)
        self.player.set_property("audio-sink", audio_sink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        audio_file = "audio.mp3"
        uri = "file://" + os.path.abspath(audio_file)
        self.player.set_property("uri", uri)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            err, debug = message.parse_qos()
            print ("Error: {0}").format (err, debug)
            self.is_playing = False
            self.player.set_state(Gst.State.NULL)
            self.label.set_text("00:00 / 00:00")
            self.scale.set_value(0)
                        
        elif t == Gst.MessageType.ERROR:
            self.is_playing = False
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print ("Error: {0}").format (err, debug)
            self.player.set_state(Gst.State.NULL)
            self.label.set_text("00:00 / 00:00")
            self.scale.set_value(0) 

    def play_pause_clicked(self, button):
        if button.get_icon_name() == "media-playback-start":
            button.set_icon_name("media-playback-pause")
            self.player.set_state(Gst.State.PLAYING)
            GLib.timeout_add(1000, self.update_gui)

            
        else: 
            button.set_icon_name("media-playback-start")
            self.player.set_state(Gst.State.PAUSED)

    def stop_clicked(self, button):
        self.player.set_state(Gst.State.NULL)
        self.button_play_pause.set_icon_name("media-playback-start")
        self.label.set_text("00:00 / 00:00")
        self.scale.set_value(0)
        
    def scale_changed(self, scale):
        seek_time = self.scale.get_value()
        self.player.seek_simple(
            Gst.Format.TIME,  
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 
            seek_time * Gst.SECOND
            )
        
        
    def update_gui(self):
        state = self.player.get_state(0.005)
        if state[1] != Gst.State.PLAYING:
            print("not playing")
            #print("State is not playing")
            return False # cancel timeout
        else:
            success, int_duration = self.player.query_duration(Gst.Format.TIME)
            success, int_position = self.player.query_position(Gst.Format.TIME)
            #update label and set scale range
            str_duration = self.convert_ns(int_duration)
            self.scale.set_range(0, int_duration / Gst.SECOND)
            
            str_position = self.convert_ns(int_position)
            self.scale.handler_block(self.scale_handler_id)
            self.scale.set_value(float(int_position) / Gst.SECOND)
            self.scale.handler_unblock(self.scale_handler_id)
            
            self.label.set_text(str_position + " / " + str_duration)
            
            return True
            
        
    def convert_ns(self, time_int):
        s,ns = divmod(time_int, 1000000000)
        m,s = divmod(s, 60)

        if m < 60:
            str_duration = "%02i:%02i" %(m,s)
            return str_duration
        else:
            h,m = divmod(m, 60)
            str_duration = "%i:%02i:%02i" %(h,m,s)
            return str_duration        


def on_activate(app):

    win = AppWindow(app)
    win.present()


app = Gtk.Application(application_id='com.example.scale')
app.connect('activate', on_activate)
app.run(None)
