#!/usr/bin/env bash
set -e
wget -O spotifycli https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/spotifycli.py
chmod +x spotifycli
sudo mv spotifycli /usr/local/bin/spotifycli
