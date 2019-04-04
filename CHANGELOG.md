CHANGELOG
=========

v. 1.4.2
--------
*04 Apr 2019*
- fixed volume control (now script controls app volume instead of system volume) - issue #10, PR #40

v. 1.4.1
--------
*07 Feb 2019*
- handling input in a different way in shell mode depending on Python version

v. 1.4.0
--------
*02 Feb 2019*
- added dependency to `lyricwikia`
- added `--lyrics` option

v. 1.3.0
--------
*22 Jan 2019*
- added shell mode

v. 1.2.7
--------
*15 Jan 2019*
- updating docs

v. 1.2.6
--------
*09 Jan 2019*
- adding classifiers to `setup.py`

v. 1.2.5
--------
*05 Jan 2019*
- updating setup.py (adding `long_description`) and simplifying release task in Makefile 

v. 1.2.4
--------
*05 Jan 2019*
- Fixing version import for Python 3.7 and higher and keeping backward-compatibility with older Python versions - fixes #32

v. 1.2.3
--------
*19 Dec 2018*
- replacing dictionary with arguments with the list of tuples because it seems to be a better structure for this purpose

v. 1.2.2
--------
*18 Dec 2018*
- refactored code: extracted script arguments into dictionary

v. 1.2.1
--------
*16 Dec 2018*
- updated project description
- updated release configuration

v. 1.2.0
--------
*15 Dec 2018*
- replaced getopts with argparse for parsing CLI arguments
- added auto-generation of the help for the script
- added `-h` param
- renamed param `--status-short` to `--statusshort`
- renamed param `--song-short` to `--songshort`
- renamed param `--artist-short` to `--artistshort`
- renamed param `--playback-status` to `--playbackstatus`
- slightly reformatted the code

v. 1.1.1
--------
*15 Dec 2018*
- updated license to GPL 3.0


v. 1.1.0
--------
*15 Dec 2018*

- added new options:
  - `--song`
  - `--song-short`
  - `--album`
  - `--artist`
  - `--artist-short`
  - `--playback-status`
- extracted version to `spotifycli/version.py` file
- removed short options:
  - `-h`
  - `-v`
- added info about utf-8 encoding to the file header
- updated script shebang from `#!/usr/bin/env python` to `#!/usr/bin/python -u` due to problems with the script execution

v. 1.0.0
--------
*30 Mar 2018*

First release of the library available on pypi

https://pypi.org/project/spotify-cli-linux/1.0.0/
