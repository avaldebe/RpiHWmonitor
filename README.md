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

## Testing on emulated hardware
Test/modify the layout and system calls on a full Linux machine.
The information is displayed on a small x-window for 15 seconds.

### Installation for python3
[luma.emulator][install.emulator]
```bash
sudo apt install python3-dev python3-pip build-essential
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
sudo pip3 install --upgrade luma.emulator
```

### Display when script is changed
`.sys_info.py` will show the emulated display only for 15 seconds.
The following commands will execute the script every time the file is saved
```bash
while inotifywait -qqre modify ./sys_info.py; do
  ./sys_info.py
done
```

## SSD1306 on a Raspberry Pi
After `.sys_info.py` is called, the display will be updated once a minute.

### Installation for python3
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
There are different options to start a job after boot, see [here](howto).
This are the ones I have tried/plan to try out.
- cronjob: easy to set-up, need to reboot to update the script
- service: harder to set-up, easy to start/stop

[howto]: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

#### Run as a cronjob
Add the following lines to your crontab (`crontab -e`)
```
@reboot bash -lc $HOME/RpiHWmonitor/sys_info.py
```
The `bash -l` is needed to get the right `$PATH` for `iwconfig`,
which in turn is needed for the wifi signal strength.

#### Run as a service
TBD
