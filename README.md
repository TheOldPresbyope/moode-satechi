# Add moOde support for the Satechi Bluetooth Multi-Media Remote

The [Satechi Bluetooth Multi-Media Remote](https://satechi.net/products/satechi-blu...dia-remote) is marketed "...for your Bluetooth iOS device."

However, it's a general-purpose BT remote which can be used to control a number of moOde playback functions.

This repo provides a script and configuration files to add Satechi support to moOde.

There are eight buttons on the device which the script maps to the following moOde functions: play/pause, previous track, next track, volume up, volume down, mute/unmute, load Favorites, and load Default Playlist. This mapping can be changed, of course.

## Prerequisites:

- Raspbian Buster (for up-to-date Python3 and Python evdev module) This requirement is fulfilled automatically by working with moOde 5.4beta series or above. In principle, one can update the Python3 subsystem on an earlier version of moOde but this effort is not addressed here.

- moOde with Bluetooth controller present and enabled. This project was developed in moOde 5.4beta2 on an RPi3B+ with its onboard controller.

- The Satechi remote paired with, connected to, and trusted by the moOde Bluetooth subsystem. See [Configuring the Satechi connection]() This need be done only once unless/until the moOde BT controller is reset. The result is preserved across reboots.

Note: Once paired, the Satechi will show up on the moOde Bluez Config screen as "Bluetooth Media Control & Camera Shutter Click". Ignore this. Obviously, it is not an audio device. Do not attempt to connect via this screen.</aside>

## Components

1. `/etc/udev/rules.42-satechi.rules`
This rule tells `udev` what to do when the virtual Linux input device representing the Satechi Remote is detected. It tells `udev` to create a symlink `/dev/SBMMR` for convenience and to invoke a `systemd` service. The symlink is removed when the remote goes to sleep or is powered off and the virtual input device is removed. (Why the number 42? Ask any reader of Douglas Adam's **Hitchhiker's Guide to the Galaxy.**)

2. `/etc/systemd/system/satechi.service` This tells `systemd` to start the actual satechi script after `udev` detects the remote and creates the symlink and to stop it when the symlink is removed.

3. `/usr/local/bin/satechi.py` This is the actual script which endlessly loops waiting for appropriate events and calls either mpc or moOde utility script(s) to carry out commands. It is started and stopped by `systemd`.

## Installation:

### The hardcore way

1. Install the Python evdev package `sudo apt-get install python3-evdev`

1. clone the repo on your RPi and cd into it
```
git clone https://github.com/theoldpresbyope/moode-satechi.git
cd moode-satechi
```

1. As superuser, copy the file `etc/udev/rules.d/42-satechi.rules` to `/etc/udev/rules.d/42-satechi.rules`
It should have permissions 644 (-rw-r--r--).

1. As superuser, copy the file `etc/systemd/system/satechi.service` to `/etc/systemd/system/satechi.service`
It should have permissions 644 (-rw-r--r--).

1. As superuser, copy the file `usr/local/bin/satechi.py` to `/usr/local/bin/satechi.py`
It should have permissions 755 (-rwxr-xr-x).

1. Reboot

1. Turn on the Satechi Remote and click a button.

### The easy way

1. clone the repo on your RPi and cd into it
```
git clone https://github.com/theoldpresbyope/moode-satechi.git
cd moode-satechi
```

2. check that install-satech.sh is executable and invoke it `./install-satech.sh`

3. Turn on the Satechi Remote and click a button.

## Notes


- It may take 2s-5s for moOde to become responsive to its commands after the remote is turned on or waked up by a button press once it's gone to sleep after a period of inactivity. Button presses will be ignored during this initial deadband, which can be disconcerting to an impatient user.

- If one wanted to use a different make/model of Bluetooth remote, one would have to determine the keycodes being output and adjust the mappings in the Python script accordingly. (With luck, all multi-media remotes emit the same basic set of keycodes but you never know.) As well, one would have to determine the specifics of the new remote's virtual-input device and adjust the rules file accordingly.

- It is possible to start up the Satechi script without resorting to `systemd`. Files needed to implement this alternative approach can be found in the `planB` subdirectory. From a performance perspective, the two approaches seem equivalent. The `systemd` approach, however, is in line with the Tao of modern Linux.
