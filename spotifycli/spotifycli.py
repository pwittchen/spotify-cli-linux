#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""a command line interface to Spotify on Linux"""

import sys
import os
import argparse
import dbus
import lyricwikia
from subprocess import Popen, PIPE, check_output

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
    elif args.volumeup:
        control_volume("+5%")
    elif args.volumedown:
        control_volume("-5%")


def start_shell():
    while(True):
        try:
            command = input('spotify > ')
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
        ("--statusshort", "shows status in a short way"),
        ("--song", "shows the song name"),
        ("--songshort", "shows the song name in a short way"),
        ("--artist", "shows artist name"),
        ("--artistshort", "shows artist name in a short way"),
        ("--album", "shows album name"),
        ("--arturl", "shows album image url"),
        ("--playbackstatus", "shows playback status"),
        ("--play", "plays the song"),
        ("--pause", "pauses the song"),
        ("--playpause", "plays or pauses the song (toggles a state)"),
        ("--lyrics", "shows the lyrics for the song"),
        ("--next", "plays the next song"),
        ("--prev", "plays the previous song"),
        ("--volumeup", "increases the sound volume"),
        ("--volumedown", "decreases the sound volume")
    ]


def show_version():
    print("1.5.0")


def get_song():
    metadata = get_spotify_property("Metadata")
    artist = metadata['xesam:artist'][0]
    title = metadata['xesam:title']
    return (artist, title)


def show_status():
    artist, title = get_song()
    print(f'{artist} - {title}')

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
        lyrics = ''.join(lyrics[0]).encode('utf-8')
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
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.%s" % client,
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


def control_volume(volume_percent):
    num = get_sink_number()
    if not num:
        print('No running Spotify instance found')
        return

    Popen(
        'pactl set-sink-input-volume {0} {1}'.format(num, volume_percent),
        shell=True,
        stdout=PIPE)


def get_sink_number():
    out = check_output(['pacmd', 'list-sink-inputs'])
    for sink in out.split('index: '):
        if 'spotify' in sink:
            sink_number = sink.split('\n')[0]
            break
    else:
        sink_number = None

    return sink_number


if __name__ == "__main__":
    main()
