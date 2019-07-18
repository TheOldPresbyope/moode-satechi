# Configuring the Satechi connection

## Synopsis of steps

1. start bluetoothctl from the command line

1. in bluetoothctl, turn scan on

1. turn on the Satechi Remote and put it in discovery mode. This is done by clicking the discover (radiating-signal icon) button revealed by sliding down the front cover.

1. in bluetoothctl, pair with the Satechi device MAC address once it's found

1. answer the challenge by entering the PIN code in the Satechi mini-keyboard and pressing its enter button. If this fails due to fat fingers or such, the challenge will be repeated with a new PIN code.

1. connect to the Satechi device

1. trust the Satechi Device

1. exit bluetoothctl

## Sample dialog

User entries follow the `[bluetoothctl]#` prompt
```
pi@moode:~ $ sudo bluetoothctl
Agent registered
[bluetooth]# scan on
Discovery started
[CHG] Controller DC:A6:32:03:17:AC Discovering: yes
[NEW] Device B8:27:EB:41:35:CF MoodeLR Bluetooth
[NEW] Device DC:2C:26:01:82:8A DC-2C-26-01-82-8A
[CHG] Device DC:2C:26:01:82:8A LegacyPairing: no
[CHG] Device DC:2C:26:01:82:8A Name: Bluetooth Media Control & Camera Shutter Click
[CHG] Device DC:2C:26:01:82:8A Alias: Bluetooth Media Control & Camera Shutter Click
[CHG] Device DC:2C:26:01:82:8A LegacyPairing: yes
[bluetooth]# pair DC:2C:26:01:82:8A
Attempting to pair with DC:2C:26:01:82:8A
[CHG] Device DC:2C:26:01:82:8A Connected: yes
[agent] PIN code: 422662
[CHG] Device DC:2C:26:01:82:8A Modalias: usb:v05ACp023Cd011B
[CHG] Device DC:2C:26:01:82:8A UUIDs: 00001000-0000-1000-8000-00805f9b34fb
[CHG] Device DC:2C:26:01:82:8A UUIDs: 00001124-0000-1000-8000-00805f9b34fb
[CHG] Device DC:2C:26:01:82:8A UUIDs: 00001200-0000-1000-8000-00805f9b34fb
[CHG] Device DC:2C:26:01:82:8A ServicesResolved: yes
[CHG] Device DC:2C:26:01:82:8A Paired: yes
Pairing successful
[CHG] Device DC:2C:26:01:82:8A ServicesResolved: no
[CHG] Device DC:2C:26:01:82:8A Connected: no
[CHG] Device DC:2C:26:01:82:8A RSSI: -63
[bluetooth]# connect DC:2C:26:01:82:8A
Attempting to connect to DC:2C:26:01:82:8A
[CHG] Device DC:2C:26:01:82:8A Connected: yes
Connection successful
[CHG] Device DC:2C:26:01:82:8A ServicesResolved: yes
[Bluetooth Media Control & Camera Shutter Click]# trust DC:2C:26:01:82:8A
[CHG] Device DC:2C:26:01:82:8A Trusted: yes
Changing DC:2C:26:01:82:8A trust succeeded
[Bluetooth Media Control & Camera Shutter Click]# exit
```

Note that other Bluetooth devices are likely to be discovered during this process. Here, for example, another moOde player was found.
