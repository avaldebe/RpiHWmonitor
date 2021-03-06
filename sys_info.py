#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display basic system information.
- host: nodename kernel-release (same as `uname -nr`)
- ip: IP address
- wifi: signal strength (RSSI) [dBm]
- cpu: mean CPU load [%], calulcated as 1 min mean load / number of cores * 100
- mem: memory usage [%], calculated as (total - available) / total * 100
- disk: disk usage [%]
- temp: CPU temperature [°C]
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

def sinfo(key):
    """
    Basic system information
    """

    host = lambda : '{0[1]} {0[2]}'.format(os.uname())

    ip = lambda : socket.gethostbyname('%s.local'%socket.gethostname())

    wifi = lambda : subprocess.check_output(
        "/sbin/iwconfig wlan0 2>/dev/null | grep Signal | sed 's:.*=::'",
        shell=True,
    ).decode('UTF-8').replace('dBm', '').strip() or 'N/A'

    cpu = lambda : '%.0f%%'%(os.getloadavg()[0]/os.cpu_count()*100)

    mem = lambda : 'MEM: %.0f%%'%psutil.virtual_memory().percent

    disk = lambda : '%.0f%%'%psutil.disk_usage("/").percent

    temp = lambda : subprocess.check_output(
        """/usr/bin/awk '{printf "%.0f°C", $0/1000}' < /sys/class/thermal/thermal_zone0/temp""",
        shell=True,
    ).decode('UTF-8')

    try:
        return dict(host=host, ip=ip, wifi=wifi, cpu=cpu, mem=mem, disk=disk, temp=temp)[key]
    except KeyError:
        return None


def stats(device, info, font):
    """
    draw system info to canvas
    """
    with canvas(device) as draw:
        for (x, y, icon, dx, dy, size, fn) in info:
            if icon:
                draw.text((x, y), icon, font=font['icon_%s'%size], fill="white")
            if fn:
                x += dx; y += dy
                draw.text((x, y), fn(), font=font['text_%s'%size], fill="white")


def main():
    try:
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        forever = True
    except NameError:
        device = pygame()
        forever = False

    # custom fonts
    font_path = "%s/fonts/%%s"%os.path.dirname(__file__)
    font = dict(
        text_small = ImageFont.truetype(font_path%'Montserrat-Light.ttf', 12),
        text_large = ImageFont.truetype(font_path%'Montserrat-Medium.ttf', 19),
        icon_small = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 14),
        icon_large = ImageFont.truetype(font_path%'fontawesome-webfont.ttf', 19),
    )

    # layout: (x, y, icon, dx, dy, size, function)
    info = (
        ( 1,  0, None    ,  0,  0, 'small', sinfo('host')),
        ( 1, 15, None    ,  0,  0, 'small', sinfo('ip')),
        ( 0, 29, '\uf2db', 22, -2, 'large', sinfo('cpu')),
        ( 0, 50, None    ,  0,  0, 'small', sinfo('mem')),
        (74, 15, '\uf1eb', 18,  0, 'small', sinfo('wifi')),
        (76, 50, '\uf1c0', 13,  0, 'small', sinfo('disk')),
        (78, 33, '\uf2c8', 10,  0, 'small', sinfo('temp')),
    )

    stats(device, info, font)
    time.sleep(15)  # 1st update after 15s
    while forever:
        stats(device, info, font)
        time.sleep(60) # update every minute


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
