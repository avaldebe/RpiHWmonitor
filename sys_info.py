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
        host='{0[1]} {0[2]}'.format(os.uname()),
#       boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%F %R"),
        ip=socket.gethostbyname('%s.local'%socket.gethostname()),
        cpu='%.0f%%'%(os.getloadavg()[0]*100),
        mem='MEM: %.0f%%'%psutil.virtual_memory().percent,
        disk='%.0f%%'%psutil.disk_usage("/").percent,
        temp=subprocess.check_output(
            """awk '{printf "%.0f°C", $0/1000}' < /sys/class/thermal/thermal_zone0/temp""",
            shell=True,
        ).decode('UTF-8'),
    )
    with canvas(device) as draw:
        for text, (xy, icon, dxy, size) in info.items():
            xy0 = xy
            xy1 = (xy[0]+dxy[0],xy[1]+dxy[1])
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
        icon_large = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 19),
    )

    # layout
    info = dict(#((x, y), icon, (dx, dy), size)
        host = (( 0,  0), ''      , ( 0,  0), 'small'),
        ip   = (( 0, 15), '\uf1eb', (18,  0), 'small'),
        cpu  = (( 0, 29), '\uf2db', (22, -2), 'large'),
        mem  = (( 0, 50), ''      , ( 0,  0), 'small'),
        disk = ((76, 50), '\uf1c0', (13,  0), 'small'),
        temp = ((78, 33), '\uf2c8', (10,  0), 'small'),
    )

    while True:
        stats(device, info, font)
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
