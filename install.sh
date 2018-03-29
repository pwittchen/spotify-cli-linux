#!/usr/bin/env bash
set -e
wget -O spotifycli https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/spotifycli.py
chmod +x spotifycli.py
sudo mv spotifycli.pl /usr/local/bin/spotifycli
