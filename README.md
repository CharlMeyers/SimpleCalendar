# SimpleCalendar

A simple calendar that can replace your printed out version on the wall.

This is a simple black and white calendar that integrates with [Google Calendar](https://developers.google.com/calendar/) to display your events. This is perfect for a e-ink calendar project.

This program generates a black and white bitmap image for display on e-ink displays. This calendar has been written in Python with the [Waveshare 7.5inch e-ink](https://www.waveshare.com/7.5inch-e-paper-hat.htm) display in mind. However this should work with any screen resolution and e-paper display, just change the imported library in [screenInterface.py](screeninterface.py) to the library used for your display. Add the imported library files to the [lib](src/lib) folder. It is also not limited to just e-ink displays, as long as your display can show bitmaps you should be fine.

## Setup notes

This project was written in Python 3.6. It relies primarily on [Python Imaging Library (PIL)](https://pypi.org/project/Pillow/) now known as Pillow, [Google Calendar API](https://developers.google.com/api-client-library/python/apis/calendar/v3) and the [Waveshare Python Display Drivers](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT) required for the e-ink display. Setup notes can be found in the included links and will also be listed below:

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

* Lastly install all python libraries required for Google Calendar API

```bash
sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```bash
pip install requests_oauthlib
```

* Install msal (Microsoft Authentication Library)

```bash
sudo pip3 install msal
```

## Running the program

To run the program simply run [main.py](main.py).

### Before running for the first time

You will need to enable Google Calendar API in your Google API Console (see [Google API Getting Started](https://developers.google.com/api-client-library/python/start/get_started) on how to enable your API key). For the application to run you need 2 things:

1. A `credentials.json` file
2. A `token.pickle` file

See [Python Quickstart](https://developers.google.com/calendar/quickstart/python) on how to create these 2 files. It is easiest to run the example code they give you and just copy over the 2 required files to your microcontroller. Add these 2 files to the [auth](src/auth) folder under [google](src/auth/google).

These files are used to authenticate against a Google account where your calendars you want to see lives on.

#### Note

This program requires font files to work. You can specify your own path to your font of choice by changing `FONT_REGULAR` and `FONT_BOLD` in [constants.py](constants.py). To guarantee the best possible text alignment download "**Segoe UI** and **Segoe UI Bold**" from [Google Fonts](https://fonts.google.com/specimen/Raleway) and put it in the [assets/fonts](src/assets/fonts) folder

#### Note

This works out of the box with [Waveshare 7.5inch e-ink](https://www.waveshare.com/7.5inch-e-paper-hat.htm), download the required [Python Library](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT) and copy `epd7in5.py` and `epdconfig.py` to the [lib](src/lib) folder. To change the library to the one you need modify [screenInterface.py](screeninterface.py) with the library required for your display.

### Tips

* To update the calendar on boot create a cron job to run your script on startup.

``` bash
crontab -e
@reboot python3 $HOME/SimpleCalendar/main.py
```

* To update the calendar daily create a cron job to run your script at midnight.

``` bash
crontab -e
@daily python3 $HOME/SimpleCalendar/main.py
```

Save the file and run `crontab -l` to make sure that the job is there. Read [https://www.tecmint.com/11-cron-scheduling-task-examples-in-linux/](https://www.tecmint.com/11-cron-scheduling-task-examples-in-linux/) for more info.

### Customization

Anything under "Customization" in [constants.py](src/constants.py) can be changed. You can change anything else under "Config" in [constants.py](src/constants.py) but it is not guaranteed that the calendar will look good without some further changes to the code.

You can specify any number of calendars in `src/calendars.id` as long as it is in the same account used to authenticate the calendar. You can also comment out any calendar id's by putting a `#` at the start of the line. **Note** `src/calendars.id` still needs to be created

## Contributing

* If you find any bug, you are free to raise an issue or fix the file yourself.
* If you are contributing, please log an issue, and assign yourself to it
* Submitting any code needs to be done trough a pull request with an issue linked to the pull request.

## Licence

This project uses the standard GNU General Public License v3.0 license.
