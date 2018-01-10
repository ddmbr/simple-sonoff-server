This is a simple Python2 script to make use of Sonoff without flashing firmware. Tornado is needed in order to run it. Install it via `sudo pip install tornado`. All the following is done in an RPi.

# Initialization

Fill in the variables in `init.sh`. Fill in the IP for your RPi, and pick a port for it.

Long-press the button on Sonoff so that the LED flashes fast. Sonoff will create a new WiFi hotspot. Connect to it (password is 12345678). Then run `init.sh`. You will get the `deviceid` in the output. With the `deviceid` obtained, fill in the variables of `sonoff-server.py`.

# Controlling Sonoff

Run `sonoff-server.py`. Your sonoff should be set up in around 10 seconds. After that, do a GET request to `https://IP:port/command_on` or `https://IP:port/command_off`. You may run it using a browser or just curl (e.g., `curl https://IP:port/command_on`).
