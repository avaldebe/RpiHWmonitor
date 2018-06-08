#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display basic system information.
"""

import os
import time
import subprocess
from luma.emulator.device import pygame
from luma.core.render import canvas
from PIL import ImageFont


def sinfo(info):
    """
    Shell scripts for system monitoring from
    https://unix.stackexchange.com/a/391529
    """
    cmd = dict(
       IP="hostname -I | cut -d\' \' -f1 | head --bytes -1",
       CPU="top -bn1 | grep load | sed 's:, : :g;s:,:.:g;' | awk '{printf \"%.0f%\", $(NF-2)*100}'",
       MEM="free -m | awk 'NR==2{printf \"MEM: %.0f%%\", $3*100/$2 }'",
       DISK="df -h | awk '$NF==\"/\"{printf \"%s\", $5}'",
       TEMP="cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"%.0f°C\", $0/1000}'",
    )[info.upper()]
    return subprocess.check_output(cmd, shell=True).decode('UTF-8')


def stats(device, info, font):
    """
    draw info to canvas
    """
    with canvas(device) as draw:
        for text, (xy0, icon, xy1, size) in info.items():
            draw.text(xy0, icon, font=font['icon_%s'%size], fill="white")
            draw.text(xy1, sinfo(text), font=font['text_%s'%size], fill="white")


def main():
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
