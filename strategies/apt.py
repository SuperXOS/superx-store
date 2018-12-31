#!/usr/bin/python3
# example how to deal with the depcache

import dbus
from gi.repository.GLib

bus = dbus.SessionBus()

bus.get_object('org.debian.apt', '/org/debian/apt')
bus.

