# -*- coding:utf-8 -*
# Galicaster, Multistream Recorder and Player
#
#       galicaster_plugin_cameracontrol/panasonic_aw_he40
#
# Copyright (c) 2017, Teltek Video Research <galicaster@teltek.es>
#
# This work is licensed under the Creative Commons Attribution-
# NonCommercial-ShareAlike 3.0 Unported License. To view a copy of
# this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California, 94105, USA.


import requests
from galicaster.core import context

class Controls:
    def __init__(self):
        conf = context.get_conf()
        self.logger = context.get_logger()
        self.url = conf.get('cameracontrol','path')
        self.zoom_levels = conf.get_int('cameracontrol','zoom_levels')
        self.max_speed_pan_tilt = conf.get_int('cameracontrol','max_speed_pan_tilt')

        r = self.send_cmd("#O")
        if r.text == "p0":
            self.send_cmd("#O1")
        self.logger.info("Connected to remote cam {}".format(self.url))

    def move(self, direction, speed_percent):
        speed = (self.max_speed_pan_tilt*speed_percent)/100
        directions = {
            "right" : (speed+50, 50),
            "left" : (-(speed-50), 50),
            "down" : (50, -(speed-50)),
            "up" : (50, speed+50),
            "up_right" : (speed+50, speed+50),
            "down_right" : (speed+50, -(speed-50)),
            "down_left" : (-(speed-50), -(speed-50)),
            "up_left" : (-(speed-50), speed+50)
        }
        self.send_cmd("#PTS{:02}{:02}".format(directions[direction][0], directions[direction][1]))

    def move_stop(self):
        self.send_cmd("#PTS5050")
        self.send_cmd("#Z50")

    def zoom(self, zoom, speed_percent):
        speed = (self.max_speed_pan_tilt*speed_percent)/100
        ztype = {
            "tele" : speed+50,
            "wide" : -(speed-50)
        }
        self.send_cmd("#Z{:02}".format(ztype[zoom]))

    def set_preset(self, preset):
        self.send_cmd("#M{:02}".format(preset))

    def load_preset(self, preset):
        self.send_cmd("#R{:02}".format(preset))

    def send_cmd(self, cmd):
        self.logger.debug("Sending command {} to url {}".format(cmd, self.url))
        r = requests.get("http://{}/cgi-bin/aw_ptz".format(self.url), params={"cmd": cmd,"res":"1"}, timeout=2)
        return r
