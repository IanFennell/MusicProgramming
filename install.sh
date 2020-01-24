#!/bin/bash

apt-get install python3.7
apt-get install fluidsynth
apt-get install git
pip install mido
git clone https://github.com/IanFennell/MusicProgramming.git
cd MusicProgramming
mkdir songs
python3 Midify_api.py
