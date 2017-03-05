#!/usr/bin/env bash
set -e
wget -O spotify-cli https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/spotify-cli
chmod +x spotify-cli
sudo mv spotify-cli /usr/local/bin/spotify-cli
