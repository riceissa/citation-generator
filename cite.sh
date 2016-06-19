#!/bin/bash

wget --quiet -O - "$1" | python3 cite.py "$1"
