# -*- coding:utf-8 -*
# Galicaster, Multistream Recorder and Player
#
#       galicaster_plugin_cameracontrol/cameracontrol
#
# Copyright (c) 2016, Teltek Video Research <galicaster@teltek.es>
#
# This work is licensed under the Creative Commons Attribution-
# NonCommercial-ShareAlike 3.0 Unported License. To view a copy of
# this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California, 94105, USA.

import Queue

from os import path
from galicaster.core import context
from galicaster.core.core import PAGES

from gi.repository import Gtk, Gdk, GObject, Pango, GdkPixbuf

from galicaster.utils.queuethread import T


dispatcher = None
conf = None
logger = None
jobs = None
event_handler = None
cam_ctrl = None

def init():
    global conf, logger, event_handler, jobs, cam_ctrl
    dispatcher = context.get_dispatcher()
    conf = context.get_conf()
    logger = context.get_logger()
    camera = conf.get('cameracontrol','camera')

    cam = __import__(camera, globals())
    cam_ctrl = cam.Controls()

    icons = ["left","right","up1","down1","up_right","up_left","down_left","down_right","plus","minus"]
    icontheme = Gtk.IconTheme()
    for name in icons:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(get_image_path(name+".svg"))
        icontheme.add_builtin_icon(name,20,pixbuf)

    dispatcher.connect('init',load_ui)
    dispatcher.connect("action-key-press", on_key_press)
    dispatcher.connect("action-key-release", on_key_release)


    event_handler = Handler()
    jobs = Queue.Queue()
    t = T(jobs)
    t.setDaemon(True)
    t.start()

def load_ui(element):
    try:
        builder = context.get_mainwindow().nbox.get_nth_page(PAGES["REC"]).gui
    except Exception:
        logger.debug("The view not exist")
        return None

    notebook = builder.get_object("data_panel")
    builder = Gtk.Builder()
    label = Gtk.Label("Camera Control")

    builder.add_from_file(get_ui_path("camera_control.glade"))
    notebook2 = builder.get_object("notebook1")
    label2 = builder.get_object("label2")
    label3 = builder.get_object("label3")
    label1 = builder.get_object("label1")
    label4 = builder.get_object("label4")
    label_style(label)
    label_style(label2, True)
    label_style(label3, True)
    label_style(label1, True, 12)
    label_style(label4, True, 12)
    notebook.append_page(notebook2,label)
    builder.connect_signals(event_handler)

    speed_zoom = builder.get_object("adjustment1")
    speed_pan_tilt = builder.get_object("adjustment2")
    speed_zoom.set_upper(100)
    speed_pan_tilt.set_upper(100)

    speed_pan_tilt.set_value(50)
    speed_zoom.set_value(50)

    grid = builder.get_object("grid1")
    size = context.get_mainwindow().get_size()
    k1 = size[0] / 1920.0
    for button in grid.get_children():
        try:
            image = button.get_children()
            if type(image[0]) == Gtk.Image:
                image[0].set_pixel_size(k1*40)
        except:
            pass

    admin = conf.get_boolean('basic','admin')
    for widget in ["grid2","grid3"]:
        for button in builder.get_object(widget):
            if admin and "save" in button.get_name():
                button.show_all()
            image = button.get_children()
            if type(image[0]) == Gtk.Image:
                image[0].set_pixel_size(int(k1*40))
            else:
                image[0].set_use_markup(True)
                image[0].modify_font(Pango.FontDescription(str(int(k1*20))))

def label_style(label, only_text=None, fsize=20):
    if not only_text:
        label.set_property("ypad",10)
        label.set_property("xpad",10)
        label.set_property("vexpand-set",True)
        label.set_property("vexpand",True)

    size = context.get_mainwindow().get_size()
    k1 = size[0] / 1920.0
    label.set_use_markup(True)
    label.modify_font(Pango.FontDescription(str(int(k1*fsize))))
    return label

pressed = False
def on_key_press(element, source, event):
    global pressed
    if context.get_mainwindow().get_current_page() == PAGES["REC"] and not pressed:
        if event.keyval == Gdk.keyval_from_name("Up"):
            pressed = True
            logger.debug("Key pressed: up")
            event_handler.on_up()

        if event.keyval == Gdk.keyval_from_name("Right"):
            pressed = True
            logger.debug("Key pressed: right")
            event_handler.on_right()

        if event.keyval == Gdk.keyval_from_name("Down"):
            pressed = True
            logger.debug("Key pressed: down")
            event_handler.on_down()

        if event.keyval == Gdk.keyval_from_name("Left"):
            pressed = True
            logger.debug("Key pressed: left")
            event_handler.on_left()

        if event.keyval == Gdk.keyval_from_name("plus"):
            pressed = True
            logger.debug("Key pressed: zoom_in")
            event_handler.zoom_in()

        if event.keyval == Gdk.keyval_from_name("minus"):
            pressed = True
            logger.debug("Key pressed: zoom_out")
            event_handler.zoom_out()

def on_key_release(element, source, event):
    global pressed
    if event.keyval == Gdk.keyval_from_name("Up") or event.keyval == Gdk.keyval_from_name("Right") or event.keyval == Gdk.keyval_from_name("Down") \
       or event.keyval == Gdk.keyval_from_name("Left") or event.keyval == Gdk.keyval_from_name("plus") or event.keyval == Gdk.keyval_from_name("minus"):
        event_handler.on_release(Gdk.keyval_name(event.keyval))
        pressed = False


zoom_speed = 0
move_speed = 0

class Handler:
    def on_press(self, *args):
        global logger
        movements = {
            "up":self.on_up,
            "down":self.on_down,
            "left":self.on_left,
            "right":self.on_right,
            "up_left":self.on_up_left,
            "up_right":self.on_up_right,
            "down_left":self.on_down_left,
            "down_right":self.on_down_right,
            "zoom_in":self.zoom_in,
            "zoom_out":self.zoom_out
        }
        movement = args[0].get_name()
        logger.debug("Button pressed: "+movement)
        self._repeat = True
        timeout = 50
        GObject.timeout_add(timeout, movements[movement])

    def on_release(self, *args):
        self._repeat = False
        jobs.queue.clear()
        try:
            key_release = args[0].get_name()
        except:
            key_release =  args[0]
        jobs.put((cam_ctrl.move_stop, (key_release,)))

    def on_up(self, *args):
        jobs.put((cam_ctrl.move, ("up", move_speed)))

    def on_right(self, *args):
        jobs.put((cam_ctrl.move, ("right", move_speed)))

    def on_down(self, *args):
        jobs.put((cam_ctrl.move, ("down", move_speed)))

    def on_left(self, *args):
        jobs.put((cam_ctrl.move, ("left", move_speed)))

    def on_up_left(self):
        jobs.put((cam_ctrl.move, ("up_left", move_speed)))

    def on_up_right(self):
        jobs.put((cam_ctrl.move, ("up_right",move_speed)))

    def on_down_left(self):
        jobs.put((cam_ctrl.move, ("down_left", move_speed)))

    def on_down_right(self):
        jobs.put((cam_ctrl.move, ("down_right", move_speed)))

    def on_load_presets(self, *args):
        preset = int(args[0].get_name().split(" ")[1])
        jobs.put((cam_ctrl.load_preset, (preset,)))
        logger.debug("Load camera preset: {}".format(preset))

    def on_save_presets(self, *args):
        preset = int(args[0].get_name().split(" ")[1])
        jobs.put((cam_ctrl.set_preset, (preset, )))
        logger.debug("Save camera preset: {}".format(preset))

    def zoom_in(self, *args):
        jobs.put((cam_ctrl.zoom, ("tele", zoom_speed)))

    def zoom_out(self, *args):
        jobs.put((cam_ctrl.zoom, ("wide", zoom_speed)))

    def on_zoom_speed(self, *args):
        global zoom_speed
        zoom_speed = int(args[0].get_value())
        logger.debug("Zoom speed set to: {}".format(zoom_speed))

    def on_move_speed(self, *args):
        global move_speed
        move_speed = int(args[0].get_value())
        logger.debug("Pan/Tilt speed set to: {}".format(move_speed))

def get_ui_path(ui_file=""):
    """Retrieve the path to the folder where glade UI files are stored.
    If a file name is provided, the path will be for the file
    """
    data_dir = path.abspath(path.join(path.dirname(__file__), "resources/ui"))
    return path.join(data_dir, ui_file)

def get_image_path(image_file=""):
    """Retrieve the path to the folder where images are stored.
    If a file name is provided, the path will be for the file
    """
    data_dir = path.abspath(path.join(path.dirname(__file__), "resources/images"))
    return path.join(data_dir, image_file)
