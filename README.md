# PicoGen

Overview
--------
Simple little tool to create a list of .picopass files to use for emulation on the Picopass app on the Flipper Zero.
Will generate the PACS string, calculate correct parity bits for each format and encrypt with legacy iCLASS transports key.
Can create files in the following PACS formats:

* h10301 - Standard 26bit
* h10306 - HID Standard 34bit
* c1k35s - HID 35bit Corporate 1000
* h10304 - HID Farpointe 37bit with Site Code
* c1k48s - HID 48bit Corporate 1000

Why is this useful?
-------------------
This is not for brute forcing a door to get initial access, thats stupid.
This is a tool to help with privilege escalation in a world where you already have a working card clone, but it wont open the big door at the back of the office, or say, the DC door.
HID nicely provide their cards in packs of 100, usually all with the same facility code, and incrementing card numbers, this is what we abuse.
If card number 23 doesnt open the door you want to, maybe card number 59 will? As these two cards were provided in the same box from HID.

Requirements
------------
Install the following python module

* pycryptodome

Usage
-----
python3 ./picogen.py -cn 100 -fc 123 -num 100 -f h10301 -o pico_files

Credit
------
The fantastic work on the PicoPass flipper app, this tool is awesome!
Eric Betts - @bettse
https://gitlab.com/bettse/picopass
