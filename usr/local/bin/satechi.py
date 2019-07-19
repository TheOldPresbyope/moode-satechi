#!/usr/bin/python3
import sys,evdev,subprocess,time

# Hackery by TheOldPresbyope, 20190712
# - Control some moOde playback functions using a Satechi Bluetooth Multi-Media Remote

# Prerequisites:
# - Raspbian Buster (for up-to-date Python3 and Python evdev module)
# - moOde Bluetooth controller present and enabled (I'm developing on an RPi3B+)
# - The Satechi remote is paired with, connected to, and trusted by the
#       moOde Bluetooth subsystem (using bluetoothctl). This need be done
#       only once unless/until the moOde BT controller is reset.

# Basics:
# - Initially, the Satechi remote is asleep.
# - A companion udev rule is triggered when the Satechi is awakened by a
#     button press and the signal is detected by moOde's BT controller;
#     the rule creates a symlink /dev/SBMMR for convenience and
#     alerts systemd which starts this script in turn.
# - When the Satechi goes back to sleep after a period of inactivity, udev
#     removes the symlink and systemd kills this script
# - This script runs forever until killed by systemd, by an explicit act by root,
#     or by a reboot
# NOTE: it seems to take some seconds after an initial button-press before
#         all the machinery is working and moOde starts responding.
#         The first press or more is lost in the warmup.

try:
    satechi=evdev.InputDevice('/dev/SBMMR')
except:
    # oops, device is gone (shouldn't happen here)
    sys.exit()

# Make sure Raspbian doesn't consume the inputs before we do
satechi.grab()

# Loop forever looking for key-down events from the Satechi, mapping the
#   resulting keycodes into moOde operations.
# The keycodes being transmitted were determined through testing.
# The keycodes are burned into the Satechi microcode and can't be changed.
# Mostly the button-icons are self-explanatory. The two which aren't are a
#   a button whose icon looks like an open rectangle, whose keycode I mapped
#   to "load Favorites" and a button whose icon looks vaguely like a
#   keyboard whose keycode I mapped to "load Default Playlist".

try:
  for event in satechi.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
      attrib = evdev.categorize(event)
      if attrib.keystate == 1:
        if attrib.keycode == 'KEY_NEXTSONG':
          subprocess.run(['mpc','-q','next'])
        elif attrib.keycode == 'KEY_PREVIOUSSONG':
          subprocess.run(['mpc','-q','prev'])
        elif attrib.keycode == 'KEY_VOLUMEUP':
          subprocess.run(['/var/www/vol.sh','-up','10'])
        elif attrib.keycode == 'KEY_VOLUMEDOWN':
          subprocess.run(['/var/www/vol.sh','-dn','10'])
        elif attrib.keycode == 'KEY_PLAYPAUSE':
          subprocess.run(['mpc','-q','toggle'])
        elif attrib.keycode == 'KEY_HOMEPAGE':
          subprocess.run(['mpc','-q','clear'])
          time.sleep(0.1)
          subprocess.run(['mpc','-q','load','Default Playlist'])
        elif attrib.keycode == 'KEY_EJECTCD':
          subprocess.run(['mpc','-q','clear'])
          time.sleep(0.1)
          subprocess.run(['mpc','-q','load', 'Favorites'])
        # careful: the Satechi returns two keycodes in a Python list
        #          when the mute button is pressed
        elif 'KEY_MUTE' in attrib.keycode:
          subprocess.run(['/var/www/vol.sh','-mute'])
except:
  # remote must have disappeared
  sys.exit()
