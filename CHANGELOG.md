CHANGELOG
=========

v. 1.9.0
--------
*17 Dec 2024*

- Add error handling in many locations, new SpotifyCLIException, and update formatting and format checker (#85)
- Add --songuri and --listuri to enable playing a song or playlist Uri (#86)
    - Add --openuri to allow specifying a song Uri to play
    - Add --listuri

v. 1.8.3
--------
*9 Dec 2024*

- Switch to pure python library for dbus - PR #82 by @allhailwesttexas (closes #53)

v. 1.8.2
--------
*1 Nov 2023*

- Search the session bus for MPRIS name - PR #79 by @flip1995

v. 1.8.1
--------
*15 Mar 2023*

- automated deployment to pypi

v. 1.8.0
--------
*11 Mar 2023*

- added --position param
- updated CI configuration

v. 1.7.1
--------
*05 Nov 2022*

- updated version number

v. 1.7.0
--------
*05 Nov 2022*

- added statusposition argument
- fixed file name in .travis.yml: checkformat.py -> check_format.py
- fixed .travis.yml CI build config
- converted bash Scripts to Python Scripts
- added double quote to prevent globbing and word splitting
- added strip method to remove blank spaces in input
- updated formatting and Makefile
- updated shebang

v. 1.6.0
--------
*22 Jun 2019*
- removed volume controls

v. 1.5.1
--------
*19 May 2019*
- fixed displaying of the lyrics - PR #48

v. 1.5.0
--------
*12 May 2019*
- performed code cleanup by re-ordering functions
- fixed grammar in docs
- replaced duplicated calls in bash scripts with loops
- updated string formatting with `print(f'...')` method - PR #44
- changed version check to all Python 3 versions - PR #46
- added function to display the image url of the album with `--arturl` parameter - PR #45
- added support for third-party clients with `--client CLIENTNAME` parameter - PR #45
- abandonned deprecated Python 2 support (Python 2.7 development will stop in 2020)
- now we're supporting Python 3 only what was reflected in the script shebang and code

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
