Raspberry Pi File Server
########################
:date: 2020-06-12 16:55
:author: Patrick Cloke
:tags: linux

This is just some quick notes (for myself) of how I recently setup my Raspberry
Pi as a file server. The goal was to have a shared folder so that a Sonos could
play music from it. The data would be backed via a microSD card plugged into
USB.

1.  Update to the `newest version of Raspberry Pi OS`_.
2.  Configure `SSH (for headless mode)`_.
3.  Use the local router to find the IP address.
4.  Add a local hostname into the router for the IP.
5.  ``ssh pi@raspberrypi``:

    1.  Update everything: ``sudo apt-get update && sudo apt-get upgrade``
    2.  Clean-up: ``sudo reboot`` then
        ``sudo apt-get autoremove && sudo apt-get autoclean``
    3.  Use ``sudo raspi-config`` to update some configuration (passwords,
        connect to WiFi, etc.)
    4.  `Mount the USB drive`_ (look down for the ``fstab`` directions). (I also
        had to install `support for exFAT`_ at this point.)
    5.  Finally, `install and configure Samba`_.

After this the drive should be `findable from the Sonos app`_.

We'll see how this works after the Raspberry Pi gets rebooted at some point,
will it:

* Have the same IP address?
* Mount the USB drive properly?

.. _newest version of Raspberry Pi OS: https://www.raspberrypi.org/downloads/
.. _SSH (for headless mode): https://www.raspberrypi.org/documentation/remote-access/ssh/README.md
.. _Mount the USB drive: https://raspberrytips.com/mount-usb-drive-raspberry-pi/
.. _support for exFAT: https://www.howtogeek.com/235655/how-to-mount-and-use-an-exfat-drive-on-linux/
.. _install and configure Samba: https://www.raspberrypi.org/documentation/remote-access/samba.md
.. _findable from the Sonos app: https://support.sonos.com/s/article/257
