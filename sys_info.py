#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
import time
from datetime import datetime

import subprocess

from luma.emulator.device import pygame
from luma.core.render import canvas
from PIL import ImageFont


def sinfo(stat):
    """
    Shell scripts for system monitoring from
    https://unix.stackexchange.com/a/391529
    """
    cmd = dict(
       IP="hostname -I | cut -d\' \' -f1 | head --bytes -1",
       CPU="top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'",
       MEM="free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'",
       DISK="df -h | awk '$NF==\"/\"{printf \"%s\", $5}'",
       TEMP="vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1",
    )[stat.upper()]
    return subprocess.check_output(cmd, shell = True )



def stats(device):
    # use custom font
    font_path = "%s/%s"%(os.path.dirname(__file__), "fonts/%s")
    font = ImageFont.truetype(font_path%'Montserrat-Light.ttf', 12)
    font2 = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 14)
    font_icon_big = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 20)
    font_text_big = ImageFont.truetype(font_path%'Montserrat-Medium.ttf', 19)


    with canvas(device) as draw:
        # Icons
        draw.text(( 0, 0), chr(61931), font=font2, fill="white")
        draw.text((50,52), chr(61888), font=font2, fill="white")
        draw.text(( 0,52), chr(62152), font=font2, fill="white")
        draw.text(( 0,15), chr(62171), font=font_icon_big, fill="white")

        # Text
        draw.text((18, 0), 'IP',  font=font, fill="white")
        draw.text((22,12), 'CPU', font=font_text_big, fill="white")
        draw.text(( 0,36), 'Mem', font=font, fill="white")
        draw.text((66,52), 'Disk', font=font, fill="white")
        try:
            draw.text((10,52), 'Temp',  font=font, fill="white")
        except KeyError:
             # not enabled/available
             pass

def main():
    while True:
        stats(device)
        time.sleep(5)


if __name__ == "__main__":
    try:
        device = pygame()
        main()
    except KeyboardInterrupt:
        pass
