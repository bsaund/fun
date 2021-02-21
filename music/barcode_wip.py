#!/usr/bin/env python3

import evdev

device = evdev.InputDevice('/dev/input/by-id/usb-GD_USB_Keyboard_V1.0-9c6d-event-kbd')
device.grab()

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
