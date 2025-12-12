#!/bin/bash

# wget --quiet -O - "$1" | cite.py "$1" | tee /dev/tty | xclip -sel clip
wget --quiet -O - "$1" | python3 /home/issa/projects/autolink/autolink.py --filetype mediawiki -C "$1" | tee /dev/tty | xclip -sel clip
