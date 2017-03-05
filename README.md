# spotify-cli-linux
A command-line interface to Spotify on Linux.

This project is inspired by the similar project called [shpotify](https://github.com/hnarayanan/shpotify), which does the same thing, but on macOS.

installation
------------

with **wget**:
```
$ sh -c "$(wget https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/install.sh -O -)"
```

with **curl**:
```
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/pwittchen/spotify-cli-linux/master/install.sh)"
```

usage
-----

run the following command from your terminal:

```
spotify-cli
```

use one of the following parameters:

```
--help, -h          shows help
--status            shows status (currently played song name and artist)
--play              plays the song
--pause             pause the song
--playpause         play or pause the song (toggling state)
--next              plays the next song
--previous, --prev  plays the previous song
--volumeup          increases sound volume
--volumedown        decreases sound volume
```
