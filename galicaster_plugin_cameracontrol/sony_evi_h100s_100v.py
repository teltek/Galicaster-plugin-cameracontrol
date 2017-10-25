# -*- coding:utf-8 -*
# Galicaster, Multistream Recorder and Player
#
#       galicaster_plugin_cameracontrol/sony_evi_h100s_100v
#
# Copyright (c) 2017, Teltek Video Research <galicaster@teltek.es>
#
# This work is licensed under the Creative Commons Attribution-
# NonCommercial-ShareAlike 3.0 Unported License. To view a copy of
# this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California, 94105, USA.

import pysca
from galicaster.core import context

class Controls:
    def __init__(self):
        conf = context.get_conf()
        self.logger = context.get_logger()
        self.path = conf.get('cameracontrol','path')
        self.zoom_levels = conf.get_int('cameracontrol','zoom_levels')
        self.max_speed_pan_tilt = int(conf.get('cameracontrol','max_speed_pan_tilt'), 16)

        pysca.connect(self.path)
        pysca.set_zoom(1,0)
        pysca.pan_tilt_home(1)
        pysca.osd_off(1)
        self.logger.info("Connected to remote cam {}".format(self.path))

    def move(self, direction, speed_percent):
        speed = (self.max_speed_pan_tilt*speed_percent)/100
        directions = {
            "right" : [speed, 0],
            "left" : [-speed, 0],
            "down" : [0, -speed],
            "up" : [0, speed],
            "up_right" : [speed, speed-2],
            "down_right" : [speed, -speed+2],
            "down_left" : [-speed, -speed+2],
            "up_left" : [-speed, speed-2]
        }
        pysca.pan_tilt(1,directions[direction][0], directions[direction][1])

    def move_stop(self):
        pysca.clear_commands(1)
        pysca.zoom(1, "stop")

    def zoom(self, zoom, speed_percent):
        speed = (self.max_speed_pan_tilt*speed_percent)/100
        pysca.zoom(1, zoom, speed)

    def set_preset(self, preset):
        pysca.set_memory(1, preset)

    def load_preset(self, preset):
        pysca.recall_memory(1, preset)
