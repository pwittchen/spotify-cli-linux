# spotify-cli-linux
A command-line interface to [Spotify](https://www.spotify.com/) on Linux.

This project is inspired by the similar project called [shpotify](https://github.com/hnarayanan/shpotify), which does similar things, but on macOS.

installation
------------

with pip (recommended):

```
pip install spotify-cli-linux
```

with **wget**:
```
sh -c "$(wget https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/install.sh -O -)"
```

with **curl**:
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/install.sh)"
```

usage
-----

run the following command from your terminal:

```
spotifycli
```

use one of the following parameters:

```
--help, -h          shows help
--version, -v       shows version
--status            shows status (currently played song name and artist)
--status-short      shows status in a short way (cuts currently played song name and artist)
--play              plays the song
--pause             pauses the song
--playpause         plays or pauses the song (toggles a state)
--next              plays the next song
--prev              plays the previous song
--volumeup          increases sound volume
--volumedown        decreases sound volume
```

solving problems
----------------

When you've seen the following error:

```
No module named dbus
```

Then try to install `python-dbus`! On Ubuntu you can do it as follows:

```
sudo apt-get install python-dbus
```

If you are using another distro, then try to install `python-dbus` with your package manager.

usage with tmux
---------------

If you want to use this script in your tmux panel, you can check [tmux-plugin-spotify](https://github.com/pwittchen/tmux-plugin-spotify).
