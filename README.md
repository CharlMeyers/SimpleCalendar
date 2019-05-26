# SimpleCalendar

A simple calendar that can replace your printed out version on the wall.

This is a simple black and white calendar that integrates with [Google Calendar](https://developers.google.com/calendar/) to display your events. This is perfect for a e-ink calendar project.

This program generates a black and white bitmap image for display on e-ink displays. This calendar has been written in Python with the [Waveshare 7.5inch e-ink](https://www.waveshare.com/7.5inch-e-paper-hat.htm) display in mind. However this should work with any screen resolution and e-paper display, just change the imported library in [screeninterface.py](screeninterface.py) to the library used for your display. It is also not limited to just e-ink displays, as long as your display can show bitmaps you should be fine.

## Setup notes

This project was written in Python 3.6. It relies primarily on [Python Imaging Library (PIL)](https://pypi.org/project/Pillow/) now known as Pillow, [Google Calendar API](https://developers.google.com/api-client-library/python/apis/calendar/v3) and the [Python Library](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT) required for the e-ink display. Setup notes can be found in the included links and will also be listed below:

### To setup on Raspberry Pi

* First install pip package manager

```bash
sudo apt-get install python3-pip
```

* Next install PIL and Pillow

```bash
sudo apt-get install python-imaging
sudo pip3 install Pillow
```

&nbsp;If you get errors installing Pillow try running (see [Pillow installation docs](https://pillow.readthedocs.io/en/latest/installation.html#linux-installation)):

```bash
sudo apt-get install libjpeg8-dev libtiff5-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev \
    tcl8.6-dev tk8.6-dev python-tk
```

* In order for the Waveshare library to work you need to enable SPI interface and GPIO interface for Python

```bash
sudo pip3 install spidev
sudo pip3 install RPi.GPIO
```

* Lastly install all pyton libraries required for Google Calendar API

```bash
sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```