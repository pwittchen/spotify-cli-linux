#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import getopt
import dbus
from subprocess import Popen, PIPE
from version import __version__


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["help", "status",
                                                      "status-short",
                                                      "song", "song-short",
                                                      "album", "artist",
                                                      "artist-short",
                                                      "playback-status",
                                                      "play", "pause",
                                                      "playpause", "next",
                                                      "prev", "volumeup",
                                                      "volumedown",
                                                      "version"])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--help"):
            show_help()
        if opt in ("--version"):
            show_version()
        elif opt == "--status":
            show_current_status()
        elif opt == "--status-short":
            show_current_status_short()
        elif opt == "--song":
            show_current_song()
        elif opt == "--song-short":
            show_current_song_short()
        elif opt == "--artist":
            show_current_artist()
        elif opt == "--artist-short":
            show_current_artist_short()
        elif opt == "--album":
            show_current_album()
        elif opt == "--playback-status":
            show_current_playback_status()
        elif opt == "--play":
            perform_spotify_action("Play")
        elif opt == "--pause":
            perform_spotify_action("Pause")
        elif opt == "--playpause":
            perform_spotify_action("PlayPause")
        elif opt == "--next":
            perform_spotify_action("Next")
        elif opt == "--prev":
            perform_spotify_action("Previous")
        elif opt == "--volumeup":
            control_volume("+5%")
        elif opt == "--volumedown":
            control_volume("-5%")


def show_help():
    print(
        '\n  spotify-cli is a command line interface for Spotify on Linux\n\n'
        '  usage:\n'
        '    --help\t\tshows help\n'
        '    --version\t\tshows version\n'
        '    --status\t\tshows status (song name and artist)\n'
        '    --status-short\tshows status in a short way\n'
        '    --song\t\tshows the current song name\n'
        '    --song-short\tshows the current song name in a short way\n'
        '    --artist\t\tshows the current artist\n'
        '    --artist-short\tshows the current artist in a short way\n'
        '    --album\t\tshows the current album\n'
        '    --playback-status\tshows the current playback status (UTF-8)\n'
        '    --play\t\tplays the song\n'
        '    --pause\t\tpauses the song\n'
        '    --playpause\t\tplays or pauses the song (toggles a state)\n'
        '    --next\t\tplays the next song\n'
        '    --prev\t\tplays the previous song\n'
        '    --volumeup\t\tincreases sound volume\n'
        '    --volumedown\tdecreases sound volume\n')


def show_version():
    print(__version__)


def get_spotify_property(p):
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(
            spotify_bus, "org.freedesktop.DBus.Properties")
        return spotify_properties.Get("org.mpris.MediaPlayer2.Player", p)
    except BaseException:
        sys.stderr.write("Spotify is off\n")
        sys.exit(1)


def get_current_song():
    metadata = get_spotify_property("Metadata")
    artist = metadata['xesam:artist'][0]
    title = metadata['xesam:title']
    return (artist, title)


def show_current_status():
    artist, title = get_current_song()
    print("%s - %s" % (artist, title))


def show_current_status_short():
    artist, title = get_current_song()
    artist = artist[:15] + (artist[15:] and '...')
    title = title[:10] + (title[10:] and '...')
    print("%s - %s" % (artist, title))


def show_current_song():
    _, title = get_current_song()
    print("%s" % title)


def show_current_song_short():
    _, title = get_current_song()
    title = title[:10] + (title[10:] and '...')
    print("%s" % title)


def show_current_artist():
    artist, _ = get_current_song()
    print("%s" % artist)


def show_current_artist_short():
    artist, _ = get_current_song()
    artist = artist[:15] + (artist[15:] and '...')
    print("%s" % artist)


def show_current_playback_status():
    playback_status = get_spotify_property("PlaybackStatus")

    if playback_status == "Playing":
        print('▶')
    elif playback_status == "Paused":
        print('▮▮')
    elif playback_status == "Stopped":
        print('■')


def show_current_album():
    metadata = get_spotify_property("Metadata")
    print("%s" % metadata['xesam:album'])


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
