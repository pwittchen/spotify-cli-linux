#!/usr/bin/python -u
# -*- coding: utf-8 -*-
"""a command line interface to Spotify on Linux"""

import sys
import argparse
import dbus
from subprocess import Popen, PIPE
from version import __version__


def main():
    args = add_arguments()
    if args.version:
        show_version()
    elif args.status:
        show_status()
    elif args.statusshort:
        show_status_short()
    elif args.song:
        show_song()
    elif args.songshort:
        show_song_short()
    elif args.artist:
        show_artist()
    elif args.artistshort:
        show_artist_short()
    elif args.album:
        show_album()
    elif args.playbackstatus:
        show_playback_status()
    elif args.play:
        perform_spotify_action("Play")
    elif args.pause:
        perform_spotify_action("Pause")
    elif args.playpause:
        perform_spotify_action("PlayPause")
    elif args.next:
        perform_spotify_action("Next")
    elif args.prev:
        perform_spotify_action("Previous")
    elif args.volumeup:
        control_volume("+5%")
    elif args.volumedown:
        control_volume("-5%")


def add_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        help="shows version number",
        action="store_true")
    parser.add_argument(
        "--status",
        help="shows song name and artist",
        action="store_true")
    parser.add_argument(
        "--statusshort",
        help="shows status in a short way",
        action="store_true")
    parser.add_argument(
        "--song",
        help="shows the song name",
        action="store_true")
    parser.add_argument(
        "--songshort",
        help="shows the song name in a short way",
        action="store_true")
    parser.add_argument(
        "--artist",
        help="shows artists name",
        action="store_true")
    parser.add_argument(
        "--artistshort",
        help="shows artist name in a short way",
        action="store_true")
    parser.add_argument(
        "--album",
        help="shows album name",
        action="store_true")
    parser.add_argument(
        "--playbackstatus",
        help="shows playback status",
        action="store_true")
    parser.add_argument(
        "--play",
        help="plays the song",
        action="store_true")
    parser.add_argument(
        "--pause",
        help="pauses the song",
        action="store_true")
    parser.add_argument(
        "--playpause",
        help="plays or pauses the song (toggles a state)",
        action="store_true")
    parser.add_argument(
        "--next",
        help="plays the next song",
        action="store_true")
    parser.add_argument(
        "--prev",
        help="plays the previous song",
        action="store_true")
    parser.add_argument(
        "--volumeup",
        help="increases sound volume",
        action="store_true")
    parser.add_argument(
        "--volumedown",
        help="decreases sound volume",
        action="store_true")
    return parser.parse_args()


def show_version():
    print(__version__)


def get_song():
    metadata = get_spotify_property("Metadata")
    artist = metadata['xesam:artist'][0]
    title = metadata['xesam:title']
    return (artist, title)


def show_status():
    artist, title = get_song()
    print("%s - %s" % (artist, title))


def show_status_short():
    artist, title = get_song()
    artist = artist[:15] + (artist[15:] and '...')
    title = title[:10] + (title[10:] and '...')
    print("%s - %s" % (artist, title))


def show_song():
    _, title = get_song()
    print("%s" % title)


def show_song_short():
    _, title = get_song()
    title = title[:10] + (title[10:] and '...')
    print("%s" % title)


def show_artist():
    artist, _ = get_song()
    print("%s" % artist)


def show_artist_short():
    artist, _ = get_song()
    artist = artist[:15] + (artist[15:] and '...')
    print("%s" % artist)


def show_playback_status():
    playback_status = get_spotify_property("PlaybackStatus")
    print({"Playing": '▶',
           "Paused": '▮▮',
           "Stopped": '■'
           }[playback_status])


def show_album():
    metadata = get_spotify_property("Metadata")
    print("%s" % metadata['xesam:album'])


def get_spotify_property(spotify_property):
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(
            spotify_bus,
            "org.freedesktop.DBus.Properties")
        return spotify_properties.Get(
            "org.mpris.MediaPlayer2.Player",
            spotify_property)
    except BaseException:
        sys.stderr.write("Spotify is off\n")
        sys.exit(1)


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
