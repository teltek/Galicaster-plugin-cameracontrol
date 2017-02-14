This is a plugin for Galicaster that allows to control a remote camera from Galicaster GUI. The plugin is designed to work with Sony EVI-H100S/100V cameras, using an implementation of VISCA protocol in python.

This plugin can be installed as a deb package or through pip installer:
	- To generate deb package
		In repository root folder execute ``sudo py2deb -r pathtorepo .``

		-r pathtorepo  path to store deb files 

		This will create the plugin deb package and debs for dependences. By default packages are stored in /tmp folder.

	- To install with pip
		In the repository root folder execute ``sudo pip install``

		or execute ``python setup.py sdist`` to generate a .tar package installable from pip

Galicaster controls the camera using the serial port, so we need to add the user galicaster to the group dialout, like follows (otherwise galicaster would need root privileges):

``sudo usermod -a -G dialout galicaster``

Also it's necessary to add this lines to conf.ini in galicaster folder to run the plugin properly:
::

	[plugins]
	cameracontrol = True

	[cameracontrol]
	path = /dev/ttyUSB0
	zoom_levels = 7
	max_speed_pan_tilt = 0x18


Galicaster Project: https://github.com/teltek/Galicaster-plugin-cameracontrol
