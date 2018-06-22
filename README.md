# System Info Display
Display basic system information on a OLED display (using [luma.oled][]),
or in a x-window (using [luma.emulator][]).

This is a re-implementation of "Raspberry Pi hardware monitoring display with icons"
by [plukas][] and "SSD1306 with Python" by [Peter Scargill][scargill].

Based on the [sys_info example][luma.examples].

[plukas]:  https://www.youtube.com/watch?v=s1hvZ9zpC2o
[SSD1306]: https://github.com/xxlukas42/RPI_SSD1306
[scargill]: https://tech.scargill.net/ssd1306-with-python/
[sys_info]:  https://github.com/rm-hull/luma.examples/blob/master/examples/sys_info.py
[luma.examples]: https://github.com/rm-hull/luma.examples
[sys_info]:  https://github.com/rm-hull/luma.examples/blob/master/examples/sys_info.py
[luma.oled]: https://github.com/rm-hull/luma.oled
[luma.emulator]: https://github.com/rm-hull/luma.emulator


### Installation for python3
[luma.emulator][install.emulator]
```bash
sudo apt install python3-dev python3-pip build-essential
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
sudo pip3 install --upgrade luma.emulator
```

[luma.olded][install.oled]
```bash
sudo apt-get install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential
sudo -H pip3 install --upgrade luma.oled
```

Additional dependencies on [Raspbian Stretch Lite][raspbian]
```bash
sudo apt-get install libopenjp2-7 libtiff5
sudo -H pip3 install psutil
```

[install.emulator]: https://luma-oled.readthedocs.io/en/latest/install.html
[install.oled]: https://luma-oled.readthedocs.io/en/latest/install.html
[raspbian]: https://www.raspberrypi.org/downloads/raspbian/

### Start after boot

Add the following lines to your crontab (`crontab -e`)
```
@reboot bash -lc $HOME/RpiHWmonitor/sys_info.py
```
The `bash -l` is needed to get the right `$PATH` for `iwconfig`,
which in turn is needed for the signal strength.
