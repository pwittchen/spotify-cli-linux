#!/usr/bin/env bash
set -e
wget -O noti.py https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/spotify-cli
chmod +x noti.py
sudo mv noti.py /usr/local/bin/spotify-cli
