# Alternative approach not using systemd

This alternative approach takes advantage of the udev verb `RUN` to run a userspace command, obviating the need for `systemd` to get involved.

There is a fly in the ointment with this approach. The userspace command (and any of its child processes) will be terminated if still running when `udev` finishes. The trick used here is to let `udev` run a startup shell script which in turn invokes the actual Python script. Using the `at now` construction in this intermediary startup shell script allows the invoked Python script to continue running after udev finishes and kills the startup script.

The two approaches can't live side-by-side. Install one or the other.

## Prerequisites

The list is the same as in the primary approach. See [the primary README.](../README.md)

## Components

1. `/etc/udev/rules.d/42-satechi.rules` This replaces the same-named rule for the primary approach. It differs in that, instead of invoking `systemd` when the Satechi Remote is detected, it uses `RUN` to invoke the startup shell script.

2. `/usr/local/bin/satechi.sh` This is the startup shell script, whose sole purpose is to invoke the actual Python script. This script does not exist in the primary approach. Using the `at now` construction here is the trick which makes the alternative approach work.

3. `/usr/local/bin/satechi.py` This is the actual Python script which as in the case of the primary approach endlessly loops waiting for appropriate events and calls either mpc or moOde utility script(s) to carry out commands. It is called by the startup shell script and dies when the symlink `/dev/SBMMR` is removed by `udev`. Except for the comments, it is the same as the script used in the primary approach.

## Installation

Look sharp. These steps are similar to but not the same as those in the primary approach. No install script is available.

1. Install both the python3 evdev package and the Raspbian do package `sudo apt-get install -y python3-evdev at`

2. Clone the repo on your RPi and cd into the planB directory (*not* the top directory)
```
git clone https://github.com/TheOldPresbyope/moode-satechi.git
cd moode-satechi/planB
```

3. As superuser, copy the file `etc/udev/rules.d/42-satechi.rules` to `/etc/udev/rules.d/42-satechi.rules` It should have permissions 0644 (-rw-r--r--).

4. As superuser, copy the file `usr/local/bin/satechi.sh` to `/usr/local/bin/satechi.sh` It should have permissions 0755 (-rwxr-xr-x).

5. As superuser, copy the file `usr/local/bin/satechi.py` to `/usr/local/bin/satechi.py` It should have permissions 0755 (-rwxr-xr-x)

6. Reboot.

7. Turn on the Satechi Remote if not on already and click a button.
