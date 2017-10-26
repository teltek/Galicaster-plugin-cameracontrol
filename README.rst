# Galicaster Plugin Cameracontrol

This is a plugin for Galicaster that allows to control a remote camera from Galicaster GUI.

Right now, the plugin works with the following cameras:

* __Sony:__
	* EVI-H100S/100V cameras, using an implementation of VISCA protocol in python.
* __Panasonic:__
	* AW-HE50
	* AW-HE120
	* AW-HE60
	* AW-HE130
	* AW-HE40
	* AW-HE65
	* AW-HE70
	* AW-UE7

## Installation

This plugin can be installed as a deb package or through pip installer:
	- To generate deb package
		In repository root folder execute ``sudo py2deb -r pathtorepo .``

		-r pathtorepo  path to store deb files

		This will create the plugin deb package and debs for dependences. By default packages are stored in /tmp folder.

	- To install with pip
		In the repository root folder execute ``sudo pip install``

		or execute ``python setup.py sdist`` to generate a .tar package installable from pip

## Configuration examples

### Sony EVI-H100S/100V

Galicaster controls the camera using the serial port, so we need to add the user galicaster to the group dialout, like follows (otherwise galicaster would need root privileges):

``sudo usermod -a -G dialout galicaster``

Also it's necessary to add this lines to conf.ini in galicaster folder to run the plugin properly:

	[plugins]
	cameracontrol = True

	[cameracontrol]
	path = /dev/ttyUSB0
	zoom_levels = 7
	max_speed_pan_tilt = 0x18
	camera = sony_evi_h100s_100v

### Panasonic AW-HE50, AW-HE120, AW-HE60, AW-HE130, AW-HE40, AW-HE65, AW-HE70, AW-UE70

	[plugins]
	cameracontrol = True

	[cameracontrol]
	path = 192.168.0.10
	zoom_levels = 49
	max_speed_pan_tilt = 49
	camera = panasonic_aw_he40

Galicaster Project: https://github.com/teltek/Galicaster-plugin-cameracontrol
