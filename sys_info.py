#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display basic system information.
"""

import os
import time
import psutil
import socket
import subprocess
from PIL import ImageFont
try:
    from luma.emulator.device import pygame
except ImportError:
    from luma.core.interface.serial import i2c
    from luma.oled.device import ssd1306
finally:
    from luma.core.render import canvas


def stats(device, info, font):
    """
    draw info to canvas
    """
    sinfo = dict(
        ip=socket.gethostbyname('%s.local'%socket.gethostname()),
        cpu='%.0f, %.0f, %.0f%%'%tuple(load*100 for load in os.getloadavg()),
        mem='MEM: %.0f%%'%psutil.virtual_memory().percent,
        disk='%.0f%%'%psutil.disk_usage("/").percent,
        temp=subprocess.check_output(
            """awk '{printf "%.0f°C", $0/1000}' < /sys/class/thermal/thermal_zone0/temp""",
            shell=True,
        ).decode('UTF-8'),
    )
    with canvas(device) as draw:
        for text, (xy0, icon, xy1, size) in info.items():
            draw.text(xy0, icon, font=font['icon_%s'%size], fill="white")
            draw.text(xy1, sinfo[text], font=font['text_%s'%size], fill="white")


def main():
    try:
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
    except NameError:
        device = pygame()

    # custom fonts
    font_path = "%s/fonts/%%s"%os.path.dirname(__file__)
    font = dict(
        text_small = ImageFont.truetype(font_path%'Montserrat-Light.ttf', 12),
        text_large = ImageFont.truetype(font_path%'Montserrat-Medium.ttf', 19),
        icon_small = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 14),
        icon_large = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 20),
    )

    # layout
    info = dict(#((x0, y0), icon, (x1, y1), size)
        ip   = (( 0,  0), '\uf1eb', (18,  0), 'small'),
        cpu  = (( 0, 15), '\uf2db', (22, 12), 'large'),
        mem  = (( 0, 36), ''      , ( 0, 36), 'small'),
        disk = ((50, 52), '\uf1c0', (66, 52), 'small'),
        temp = (( 0, 52), '\uf2c8', (10, 52), 'small'),
    )

    while True:
        stats(device, info, font)
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
