# pinephone-misc
A loose collection of scripts and GUI programs to try to make things a little smoother for me using the Pinephone as my primary phone. Some of these scripts use "tk" for the GUI, so:

	sudo apt-get install python3-tk

## pinephone_misc.py
A simple Python3 + TK program to launch some common command line tasks for the Pinephone. The installer should take care of “sudo” access for newly created command. To install:

	./pinephone_misc.py install

You may need to log out and on again for commands that need “sudo” access to work.

## torish-browser.sh
If you are afraid to use the user created ARM64 port of the Tor Browser, “torish-browser.sh” might be slightly better than nothing. It will launch firefox using proxychains and tor. It doesn’t do anything else to protect the user, so you can still be fingerprinted based on other information leaked by the browser. So use at your own risk.

	./torish-browser.sh install

You may need to log out and on again for it to work.

## bin/fastcharge
Enable Fast charging. If I recall, it is (or was) useful with the keyboard case.

## bin/mntc
Decrypt and mount an encrypted sd card. Will prompt for the pass phrase. 
