---
title: Reviving My Raspberry Pi 3B
description: Reviving My Raspberry Pi 3B: From Jessie to Bookworm (and a Dead SD Card)
topic: Journal
date: 2025-09-05
hero: /img/004/hero.png
---

## TL;DR

Tried upgrading my old Raspberry Pi 3B, discovered it was still running Raspbian Jessie (2015!), installed Bookworm Lite, enabled SSH, and hit a wall when the SD card died during upgrade. 
Next step: reinstalling Raspberry Pi OS on an external drive to avoid future storage issues.

---

## The Surprise: Jessie in 2025?

I was hoping for a quick upgrade—just enable SSH and get going. But of course, things didn’t go as planned.

Turns out the OS installed was **Raspbian Jessie**, released back in 2015 and last updated in 2017. **What?!** Honestly, I thought I had used it more recently. Time flies 😅

---

## Installing the Latest Raspberry Pi OS

I headed to the official Raspberry Pi OS page [Raspberry Pi Operating Systems](https://www.raspberrypi.com/software/) for a lite environment. 
I want to save as much space and CPU as possible for Docker (or other lightweight services).

---

## Using Raspberry Pi Imager

- Formatted the SD card (32GB > FAT32).
- Had to switch USB ports, apparently Raspberry Pi Imager [doesn’t like USB3](http://reddit.com/r/rasberrypi/comments/13bmqsh/error_writing_to_storage/).
- Inserted the SD card, booted the Pi… and SSH worked! Victory! 👑


![Pi Imager screenshot](/img/004/pi-imager.png){width=679 height=475}


---

## Quick System Upgrade… or Not

I ran the usual upgrade commands:
```cmd
sudo apt-get update
sudo apt-get upgrade
```
But then… upgrade failed 😱
```
dpkg: error processing archive ... Input/output error
dpkg: error while cleaning up: unable to securely remove ... Input/output error
```
Even sudo stopped working:
```
/usr/bin/sudo: Input/output error
```

---

## Diagnosis: Dying SD Card
After some research, it seems the SD card is dying. I’ll need to buy a new one—and next time, I’ll install the OS on an external drive to avoid these read/write issues.

This video might just save my life:
[Boot Raspberry Pi from USB](https://www.youtube.com/watch?v=NDcI9HZPRaQ&t=81s)

---

## Lessons Learned
- Always check your OS version—time flies!
- SD cards wear out. Use external storage for reliability.
- Raspberry Pi Imager has quirks (USB3 issues).
- SSH can be enabled directly in the Imager—super handy.

---

## What’s Next?
Reinstalling Raspberry Pi OS on an external drive.
Stay tuned for the next post maybe this time I will progress 🤪
