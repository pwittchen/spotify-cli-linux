# spotify-cli-linux

[![Build Status](https://img.shields.io/travis/pwittchen/spotify-cli-linux.svg?branch=master&style=flat-square)](https://travis-ci.org/pwittchen/spotify-cli-linux) [![Version](https://img.shields.io/pypi/v/spotify-cli-linux.svg?style=flat-square)](https://pypi.python.org/pypi/spotify-cli-linux/) [![Python versions](https://img.shields.io/pypi/pyversions/spotify-cli-linux.svg?style=flat-square)](https://pypi.python.org/pypi/spotify-cli-linux/)

A command line interface to [Spotify](https://www.spotify.com/) on Linux.

This project is inspired by the similar project called [shpotify](https://github.com/hnarayanan/shpotify), which does similar things, but on macOS.

installation
------------

```
pip install spotify-cli-linux
```

**hint #1**: if you encounter problems during installation, try to call command with `sudo`

**hint #2**: if you still have problems (e.g. with resolving project dependencies), try to call `pip3` instead of `pip`

if you have any problems with `pip` or `pip3`, you can try to install the script in the alternative way as a workaround:

```
git clone git@github.com:pwittchen/spotify-cli-linux.git
cd spotify-cli-linux
sudo cp spotifycli/spotifycli.py /usr/local/bin/spotifycli
```

upgrade
-------

```
pip install spotify-cli-linux --upgrade
```

for the upgrade, you can apply the same hints like for installation

usage
-----

start the official Spotify desktop app

run the following command from your terminal:

```
spotifycli
```

use one of the following parameters:

```
-h, --help        show this help message and exit
--version         shows version number
--status          shows song name and artist
--statusshort     shows status in a short way
--statusposition  shows song name and artist, with current playback position
--song            shows the song name
--songshort       shows the song name in a short way
--artist          shows artists name
--artistshort     shows artist name in a short way
--album           shows album name
--arturl          shows album image url
--lyrics          shows lyrics for the song playing
--playbackstatus  shows playback status
--play            plays the song
--pause           pauses the song
--playpause       plays or pauses the song (toggles a state)
--next            plays the next song
--prev            plays the previous song
--client CLIENT   sets client's dbus name
```

if you don't use any parameters, you'll enter the shell mode, where you'll be able to use all commands mentioned above

solving problems
----------------

### dbus

When you've seen the following error:

```
No module named dbus
```

Then try to install `python-dbus`! On Ubuntu you can do it as follows:

```
sudo apt-get install python-dbus
```

If you are using another distro, then try to install `python-dbus` with your package manager.

### lyricwikia

When, you're missing `lyricwikia` dependency, run the following command:

```
pip install lyricwikia
```

usage with tmux
---------------

If you want to use this script in your tmux panel, you can check [tmux-plugin-spotify](https://github.com/pwittchen/tmux-plugin-spotify).

development
-----------

to install necessary tools for code formatting, static code analysis and releasing, run:

```
make requirements
```

code formatting
---------------

Source code should be formatted according to [PEP8](https://www.python.org/dev/peps/pep-0008/) style guides.

To format code, run:

```
make format
```

to verify code formatting, type:

```
make checkformat
```

static code analysis
--------------------

To run static code analysis, execute:

```
make lint
```

docs
----

to update docs on `gh-pages`, type:

```
make docs
```

to run docs locally, type:
```
git checkout gh-pages && ./serve.sh
```

and view page with docs at: 0.0.0.0:8000

view it on-line at https://pwittchen.github.io/spotify-cli-linux

releasing
---------

configure your `~/.pypirc` file as follows:

```
[distutils]
index-servers =
    pypi
[pypi]
username:yourusername
password:yourpassword
```

then, update version in `spotifycli/version.py` and `spotifycli/spotifycli.py` and type:

```
make release
```

**note**: Version is not kept in a single file due to problems with importing files within another file and distributing them to PyPi. There are also Python vesion issues. If you know how to fix this issue properly to keep version in one place, I'd be happy to review your PR :-).
