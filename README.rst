Galicaster Plugin Cameracontrol
===============================

This is a plugin for Galicaster that allows to control a remote camera from Galicaster GUI.

Right now, the plugin works with the following cameras:

- Sony:
	- EVI-H100S/100V cameras, using an implementation of VISCA protocol in python.
- Panasonic:
	- AW-HE50
	- AW-HE120
	- AW-HE60
	- AW-HE130
	- AW-HE40
	- AW-HE65
	- AW-HE70
	- AW-UE7

Installation
------------

This plugin can be installed as a deb package or through pip installer:
	- To generate deb package
		In repository root folder execute ``sudo py2deb -r pathtorepo .``

		-r pathtorepo  path to store deb files

		This will create the plugin deb package and debs for dependences. By default packages are stored in /tmp folder.

	- To install with pip
		In the repository root folder execute ``sudo pip install`` or execute ``python setup.py sdist`` to generate a .tar package installable from pip

Configuration examples
----------------------

Sony EVI-H100S/100V
-------------------

Galicaster controls the camera using the serial port, so we need to add the user galicaster to the group dialout, as follows (otherwise galicaster would need root privileges):

``sudo usermod -a -G dialout galicaster``

The following lines must also be added to the ``conf.ini`` file so that the plugin runs properly:
::
	[plugins]
	cameracontrol = True

	[cameracontrol]
	path = /dev/ttyUSB0
	zoom_levels = 7
	max_speed_pan_tilt = 0x18
	camera = sony_evi_h100s_100v

Panasonic AW-HE50, AW-HE120, AW-HE60, AW-HE130, AW-HE40, AW-HE65, AW-HE70, AW-UE70
----------------------------------------------------------------------------------

Add to the ``conf.ini``:
::
	[plugins]
	cameracontrol = True

	[cameracontrol]
	path = 192.168.0.10
	zoom_levels = 49
	max_speed_pan_tilt = 49
	camera = panasonic_aw_he40

Galicaster Project: https://github.com/teltek/Galicaster-plugin-cameracontrol
