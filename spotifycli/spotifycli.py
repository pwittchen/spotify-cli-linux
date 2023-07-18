#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a command line interface to Spotify on Linux"""

import argparse
import os
import sys
import datetime
from subprocess import Popen, PIPE

import dbus
import lyricwikia


def main():
    if len(sys.argv) == 1:
        start_shell()
        return 0

    global client
    args = add_arguments()
    client = args.client
    if args.version:
        show_version()
    elif args.status:
        show_status()
    elif args.statusshort:
        show_status_short()
    elif args.statusposition:
        show_status_position()
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
    elif args.position:
        show_position()
    elif args.playbackstatus:
        show_playback_status()
    elif args.lyrics:
        show_lyrics()
    elif args.arturl:
        show_art_url()
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


def start_shell():
    while True:
        try:
            command = input('spotify > ').strip()
        except EOFError:
            print("Have a nice day!")
            exit(0)

        pid = os.fork()

        if pid == 0:  # if executing context is child process
            os.execlp('spotifycli', 'spotifycli', '--{}'.format(command))
        elif pid > 0:
            os.waitpid(pid, 0)  # wait for child to exit
        else:
            print("Error during call to fork()")
            exit(1)


def add_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in get_arguments():
        parser.add_argument(argument[0], help=argument[1], action="store_true")
    parser.add_argument("--client", action="store", dest="client",
                        help="sets client's dbus name", default="spotify")
    return parser.parse_args()


def get_arguments():
    return [
        ("--version", "shows version number"),
        ("--status", "shows song name and artist"),
        ("--statusposition", "shows song name and artist, with current playback position"),
        ("--statusshort", "shows status in a short way"),
        ("--song", "shows the song name"),
        ("--songshort", "shows the song name in a short way"),
        ("--artist", "shows artist name"),
        ("--artistshort", "shows artist name in a short way"),
        ("--album", "shows album name"),
        ("--position", "shows song position"),
        ("--arturl", "shows album image url"),
        ("--playbackstatus", "shows playback status"),
        ("--play", "plays the song"),
        ("--pause", "pauses the song"),
        ("--playpause", "plays or pauses the song (toggles a state)"),
        ("--lyrics", "shows the lyrics for the song"),
        ("--next", "plays the next song"),
        ("--prev", "plays the previous song")
    ]


def show_version():
    print("1.8.1")


def get_song():
    metadata = get_spotify_property("Metadata")
    artist = metadata['xesam:artist'][0]
    title = metadata['xesam:title']
    return (artist, title)


def show_status():
    artist, title = get_song()
    print(f'{artist} - {title}')

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)

def show_status_position():
    metadata = get_spotify_property("Metadata")
    position_raw = get_spotify_property("Position")

    artist = metadata['xesam:artist'][0]
    title = metadata['xesam:title']

    # Both values are in microseconds
    position = datetime.timedelta(milliseconds=position_raw / 1000)
    length = datetime.timedelta(milliseconds=metadata['mpris:length'] / 1000)

    p_hours, p_minutes, p_seconds = convert_timedelta(position)
    l_hours, l_minutes, l_seconds = convert_timedelta(length)

    if l_hours != "00":
        # Only show hours if the song is more than an hour long
        print(f'{artist} - {title} ({p_hours}:{p_minutes}:{p_seconds}/{l_hours}:{l_minutes}:{l_seconds})')
    else:
        print(f'{artist} - {title} ({p_minutes}:{p_seconds}/{l_minutes}:{l_seconds})')


def show_status_short():
    artist, title = get_song()
    artist = artist[:15] + (artist[15:] and '...')
    title = title[:10] + (title[10:] and '...')
    print(f'{artist} - {title}')


def show_song():
    _, title = get_song()
    print(f'{title}')


def show_song_short():
    _, title = get_song()
    title = title[:10] + (title[10:] and '...')
    print(f'{title}')


def show_lyrics():
    try:
        artist, title = get_song()
        lyrics = lyricwikia.get_all_lyrics(artist, title)
        lyrics = ''.join(lyrics[0])
        print(lyrics)
    except BaseException:
        print('lyrics not found')


def show_artist():
    artist, _ = get_song()
    print(f'{artist}')


def show_artist_short():
    artist, _ = get_song()
    artist = artist[:15] + (artist[15:] and '...')
    print(f'{artist}')


def show_playback_status():
    playback_status = get_spotify_property("PlaybackStatus")
    print({"Playing": '▶',
           "Paused": '▮▮',
           "Stopped": '■'
           }[playback_status])


def show_album():
    metadata = get_spotify_property("Metadata")
    album = metadata['xesam:album']
    print(f'{album}')


def show_art_url():
    metadata = get_spotify_property("Metadata")
    print("%s" % metadata['mpris:artUrl'])


def get_spotify_property(spotify_property):
    try:
        session_bus = dbus.SessionBus()
        names = dbus.Interface(
            session_bus.get_object(
                "org.freedesktop.DBus",
                "/org/freedesktop/DBus"),
            "org.freedesktop.DBus").ListNames()
        mpris_name = None

        for name in names:
            if name.startswith("org.mpris.MediaPlayer2.%s" % client):
                mpris_name = name

        if mpris_name is None:
            sys.stderr.write("No mpris clients found for client %s\n" % client)
            sys.exit(1)

        spotify_bus = session_bus.get_object(
            mpris_name,
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
    Popen('dbus-send --print-reply --dest=org.mpris.MediaPlayer2."%s" ' %
          client +
          '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."%s"' %
          spotify_command, shell=True, stdout=PIPE)

def show_position():
    metadata = get_spotify_property("Metadata")
    position_raw = get_spotify_property("Position")
    # Both values are in microseconds
    position = datetime.timedelta(milliseconds=position_raw / 1000)
    length = datetime.timedelta(milliseconds=metadata['mpris:length'] / 1000)

    p_hours, p_minutes, p_seconds = convert_timedelta(position)
    l_hours, l_minutes, l_seconds = convert_timedelta(length)

    if l_hours != "00":
        # Only show hours if the song is more than an hour long
        print(f'({p_hours}:{p_minutes}:{p_seconds}/{l_hours}:{l_minutes}:{l_seconds})')
    else:
        print(f'({p_minutes}:{p_seconds}/{l_minutes}:{l_seconds})')


if __name__ == "__main__":
    main()
