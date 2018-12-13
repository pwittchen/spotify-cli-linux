#!/usr/bin/env python

import sys
import getopt
import dbus
from subprocess import Popen, PIPE


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvspnud", ["help", "status",
                                                         "status-short",
                                                         "play", "pause",
                                                         "playpause", "next",
                                                         "prev", "volumeup",
                                                         "volumedown",
                                                         "version"])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
        if opt in ("-v", "--version"):
            show_version()
        elif opt in ("-s", "--status"):
            show_current_song()
        elif opt == "--status-short":
            show_current_song_short()
        elif opt == "--play":
            perform_spotify_action("Play")
        elif opt == "--pause":
            perform_spotify_action("Pause")
        elif opt in ("-p", "--playpause"):
            perform_spotify_action("PlayPause")
        elif opt in ("-n", "--next"):
            perform_spotify_action("Next")
        elif opt == "--prev":
            perform_spotify_action("Previous")
        elif opt in ("-u", "--volumeup"):
            control_volume("+5%")
        elif opt in ("-d", "--volumedown"):
            control_volume("-5%")


def show_help():
    print (
        '\n  spotify-cli is a command line interface for Spotify on Linux\n\n'
        '  usage:\n'
        '    --help, -h\t\tshows help\n'
        '    --version, -v\tshows version\n'
        '    --status, -s\tshows status (song name and artist)\n'
        '    --status-short\tshows status in a short way\n'
        '    --play\t\tplays the song\n'
        '    --pause\t\tpauses the song\n'
        '    --playpause, -p\tplays or pauses the song (toggles a state)\n'
        '    --next, -n\t\tplays the next song\n'
        '    --prev\t\tplays the previous song\n'
        '    --volumeup, -u\tincreases sound volume\n'
        '    --volumedown, -d\tdecreases sound volume\n')


def show_version():
    print ('1.0.0')


def get_current_song():
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(
            spotify_bus, "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get(
            "org.mpris.MediaPlayer2.Player", "Metadata")

        artist = metadata['xesam:artist'][0]
        title = metadata['xesam:title']
        return (artist, title)
    except BaseException:
        # we go here when spotify is turned off,
        # not installed or we cannot access dbus
        return ("-", "-")


def is_spotify_available():
    artist, title = get_current_song()
    return not(artist == "-" and title == "-")


def show_current_song():
    if(is_spotify_available()):
        artist, title = get_current_song()
        print ("%s - %s" % (artist, title))
    else:
        print ("spotify is off")


def show_current_song_short():
    if(is_spotify_available()):
        artist, title = get_current_song()
        artist = artist[:15] + (artist[15:] and '...')
        title = title[:10] + (title[10:] and '...')
        print ("%s - %s" % (artist, title))
    else:
        print ("spotify is off")


def perform_spotify_action(spotify_command):
    Popen('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
          '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."%s"' %
          spotify_command, shell=True, stdout=PIPE)


def control_volume(volume_percent):
    Popen(
        'pactl set-sink-volume 0 "%s"' %
        volume_percent,
        shell=True,
        stdout=PIPE)


if __name__ == "__main__":
    main()
