#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a command line interface to Spotify on Linux"""

import argparse
import os
import sys
import textwrap
import datetime
from subprocess import Popen, PIPE

import lyricwikia

from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection


class SpotifyCLIException(Exception):
    """An exception wrapper purely to handle known exceptions nicely"""
    pass


def main():
    if len(sys.argv) == 1:
        start_shell()
        return 0

    global client
    args = add_arguments()
    client = args.client
    success = True
    try:
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
        elif args.songuri:
            song_specifier = f"string:spotify:track:{args.songuri}"
            perform_spotify_action("OpenUri", song_specifier)
        elif args.listuri:
            list_specifier = f"string:spotify:playlist:{args.listuri}"
            perform_spotify_action("OpenUri", list_specifier)
    except SpotifyCLIException as e:
        # When SpotifyCLIException is raised, we can assume these are
        # known issues, and the exception text is sufficiently helpful.
        # We can skip printing the bulky traceback by catching and only
        # printing the string repr.
        sys.stderr.write(str(e))
        success = False
    except Exception as e:
        # Then all other exceptions are handled here, and we just let Python
        # splatter the exception with the default traceback and everything.
        raise e from None

    return 0 if success else 1


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
        if len(argument) > 2 and argument[2]:
            arg_type = 'store'
        else:
            arg_type = 'store_true'

        parser.add_argument(
            argument[0],
            help=argument[1],
            action=arg_type
        )

    parser.add_argument(
        "--client",
        action="store",
        dest="client",
        help="sets client's dbus name",
        default="spotify"
    )

    return parser.parse_args()


def get_arguments():
    return [
        ("--version", "shows version number"),
        ("--status", "shows song name and artist"),
        (
            "--statusposition",
            "shows song name and artist, with current playback position"
        ),
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
        ("--prev", "plays the previous song"),
        ("--songuri", "plays the track at the provided Uri", True),
        ("--listuri", "plays the playlist at the provided Uri", True),
    ]


def show_version():
    print("1.9.1")


def get_song():
    metadata = get_spotify_property("Metadata")
    artist = ", ".join(metadata['xesam:artist'][1])
    title = metadata['xesam:title'][1]
    return artist, title


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

    artist, title = get_song()

    # Both values are in microseconds
    position = datetime.timedelta(milliseconds=position_raw / 1000)
    length = datetime.timedelta(
        milliseconds=metadata['mpris:length'][1] / 1000
    )

    p_hours, p_minutes, p_seconds = convert_timedelta(position)
    l_hours, l_minutes, l_seconds = convert_timedelta(length)

    if l_hours != "00":
        # Only show hours if the song is more than an hour long
        current = f"{p_hours}:{p_minutes}:{p_seconds}"
        full = f"{l_hours}:{l_minutes}:{l_seconds}"
        print(f'{artist} - {title} ({current}/{full})')
    else:
        current = f"{p_minutes}:{p_seconds}"
        full = f"{l_minutes}:{l_seconds}"
        print(f'{artist} - {title} ({current}/{full})')


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
    artist, title = get_song()
    try:
        lyrics = lyricwikia.get_all_lyrics(artist, title)
    except lyricwikia.LyricsNotFound:
        raise SpotifyCLIException(
            'Lyrics not found or could not connect'
        ) from None
    lyrics = ''.join(lyrics[0])
    print(lyrics)


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
    album = metadata['xesam:album'][1]
    print(f'{album}')


def show_art_url():
    metadata = get_spotify_property("Metadata")
    print("%s" % metadata['mpris:artUrl'][1])


def get_spotify_property(spotify_property):
    dbus_addr = DBusAddress(
        bus_name="org.freedesktop.DBus",
        object_path="/org/freedesktop/DBus",
        interface="org.freedesktop.DBus",
    )
    connection = open_dbus_connection(bus="SESSION")

    list_names_call = new_method_call(
        remote_obj=dbus_addr, method="ListNames", signature=""
    )
    reply = connection.send_and_get_reply(list_names_call)
    if reply.header.message_type.name == 'error':
        raise SpotifyCLIException(
            "Could not retrieve list of services (bus names) from dbus." +
            f"Full error text:\n{reply.header.message}"
        )
    names = reply.body[0]

    client_name = f"org.mpris.MediaPlayer2.{client}"
    mpris_name = next(
        (name for name in names if name.startswith(client_name)), None
    )
    if mpris_name is None:
        raise SpotifyCLIException(
            f"No mpris clients found for {client}, is {client} running?\n")

    spotify_dbus_addr = DBusAddress(
        bus_name=mpris_name,
        object_path="/org/mpris/MediaPlayer2",
        interface="org.freedesktop.DBus.Properties"
    )
    get_property_call = new_method_call(
        remote_obj=spotify_dbus_addr,
        method="Get",
        signature="ss",
        body=("org.mpris.MediaPlayer2.Player", spotify_property)
    )
    reply = connection.send_and_get_reply(get_property_call)
    if reply.header.message_type.name == 'error':
        err = '>  ' + ' ...\n>  '.join(textwrap.wrap(reply.body[0], 120))
        if 'AppArmor policy prevents' in reply.body[0]:
            info = "Could not connect to Spotify instance.\n"
            info += "It appears AppArmor has the current app sandboxed.\n"
            info += "This can block method calls via dbus.\n"
            info += "Try running from a different environment,\n"
            info += " like the default terminal.\n"
            info += "Info about AppArmor and sandboxing can be found at:\n"
            info += " https://ubuntu.com/core/docs/security-and-sandboxing\n"
            info += f"Full system response:\n{err}"
            raise SpotifyCLIException(info)
        else:
            raise SpotifyCLIException(
                f"Could not connect to Spotify instance, full response:\n{err}"
            )

    body = reply.body[0]
    return body[1]


def perform_spotify_action(spotify_command, extra_arg=None):
    command_list = [
        "dbus-send",
        "--print-reply",
        f"--dest=org.mpris.MediaPlayer2.{client}",
        "/org/mpris/MediaPlayer2",
        f"org.mpris.MediaPlayer2.Player.{spotify_command}",
    ]
    if extra_arg is not None:
        command_list.append(extra_arg)
    # could avoid this by taking out shell=False below
    # but I don't want to stomp on any of the shell side effects
    command_string = " ".join(command_list)
    Popen(command_string, shell=True, stdout=PIPE)


def show_position():
    metadata = get_spotify_property("Metadata")
    position_raw = get_spotify_property("Position")
    # Both values are in microseconds
    position = datetime.timedelta(milliseconds=position_raw / 1000)
    length = datetime.timedelta(
        milliseconds=metadata['mpris:length'][1] / 1000
    )

    p_hours, p_minutes, p_seconds = convert_timedelta(position)
    l_hours, l_minutes, l_seconds = convert_timedelta(length)

    if l_hours != "00":
        # Only show hours if the song is more than an hour long
        current = f'{p_hours}:{p_minutes}:{p_seconds}'
        full = f'{l_hours}:{l_minutes}:{l_seconds}'
        print(f'({current}/{full})')
    else:
        print(f'({p_minutes}:{p_seconds}/{l_minutes}:{l_seconds})')


if __name__ == "__main__":
    main()
