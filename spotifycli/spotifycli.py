#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import argparse
import dbus
from subprocess import Popen, PIPE
from version import __version__


parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version=__version__)
parser.add_argument('--status', dest='status', action='store_true',
                    help='shows status (song name and artist)')
parser.add_argument('--status-short', dest='status_short', action='store_true',
                    help='shows status in a short way')
parser.add_argument('--song', dest='song', action='store_true',
                    help='shows the current song')
parser.add_argument('--song-short', dest='song_short', nargs='?', const=10,
                    type=int, metavar='SONG_LEN',
                    help='shows the current song in a short way \
                            (default: 10)')
parser.add_argument('--artist', dest='artist', action='store_true',
                    help='shows the current artist')
parser.add_argument('--artist-short', dest='artist_short', nargs='?', const=15,
                    type=int, metavar='ARTIST_LEN',
                    help='shows the current artist in a short way \
                            (default: 15)')
parser.add_argument('--album', dest='album', action='store_true',
                    help='shows the current album')
parser.add_argument('--playback-status', dest='playback_status',
                    action='store_true',
                    help='shows the current playback status (UTF-8)')
parser.add_argument('--play', dest='play', action='store_true',
                    help='plays the song')
parser.add_argument('--pause', dest='pause', action='store_true',
                    help='pauses the song')
parser.add_argument('--playpause', dest='playpause', action='store_true',
                    help='plays or pauses the song (toggles a state)')
parser.add_argument('--next', dest='next', action='store_true',
                    help='plays the next song')
parser.add_argument('--prev', dest='prev', action='store_true',
                    help='plays the previous song')
parser.add_argument('--volumeup', dest='volumeup', action='store_true',
                    help='increases sound volume')
parser.add_argument('--volumedown', dest='volumedown',
                    action='store_true', help='decreases sound volume')


def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if args.status:
        show_current_status()
    elif args.status_short:
        show_current_status_short()
    elif args.song:
        show_current_song()
    elif args.song_short:
        show_current_song_short(args.song_short)
    elif args.artist:
        show_current_artist()
    elif args.artist_short:
        show_current_artist_short(args.artist_short)
    elif args.album:
        show_current_album()
    elif args.playback_status:
        show_current_playback_status()
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


def show_current_song_short(length):
    _, title = get_current_song()
    title = title[:length] + (title[length:] and '...')
    print("%s" % title)


def show_current_artist():
    artist, _ = get_current_song()
    print("%s" % artist)


def show_current_artist_short(length):
    artist, _ = get_current_song()
    artist = artist[:length] + (artist[length:] and '...')
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
