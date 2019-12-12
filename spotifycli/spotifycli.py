#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a command line interface to Spotify on Linux"""

import argparse
import os
import sys
import unicodedata as ud
import psutil
import dbus
import lyricwikia
import lyricsgenius as lg
import re
import urllib.request

from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from os.path import expanduser

TOKEN_ENV_VAR = "GENIUS_API_TOKEN"
TOKEN_FILE_NAME = ".token"
SPOTIFY_OFF_STR = "Spotify is off\n"
NO_LYRICS_STR = "lyrics not found"


def main():
    if len(sys.argv) == 1:
        start_shell()
        return 0

    global client
    args = add_arguments()
    client = args.client

    if args.version:
        show_version()
    elif args.token:
        set_genius_token(args.token)

    if spotify_is_running():
        load_genius_token()

        if args.status:
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
        elif args.export:
            export_lyrics()
    else:
        print(SPOTIFY_OFF_STR)


def start_shell():
    load_genius_token()

    while True:
        try:
            command = input("spotify > ")
        except EOFError:
            print("Have a nice day!")
            exit(0)

        if command.replace(" ", "") != "":
            pid = os.fork()

            if pid == 0:  # if executing context is child process
                os.execlp("spotifycli", "spotifycli", "--{}".format(command))
            elif pid > 0:
                os.waitpid(pid, 0)  # wait for child to exit
            else:
                print("Error during call to fork()")
                exit(1)


def add_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in get_arguments():
        parser.add_argument(argument[0], help=argument[1], action="store_true")
    parser.add_argument(
        "--client",
        action="store",
        dest="client",
        help="sets client's dbus name",
        default="spotify",
    )
    parser.add_argument("--token", type=str, help="Store genius API token")
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
        ("--export", "export lyrics"),
    ]


def set_genius_token(token):
    os.environ[TOKEN_ENV_VAR] = token

    with open(os.path.join(expanduser("~"), TOKEN_FILE_NAME), "w") as f:
        f.write(token)

    print("Token was set")


def load_genius_token():
    file_path = os.path.join(expanduser("~"), TOKEN_FILE_NAME)

    if os.path.isfile(file_path):
        with open(os.path.join(expanduser("~"), TOKEN_FILE_NAME), "r") as f:
            os.environ[TOKEN_ENV_VAR] = f.read()
    else:
        print(
            "No genius api token was set. Some lyrics will not be found. "
            "Use --token option to set it!"
        )


def show_version():
    print("1.6.0")


def get_song():
    metadata = get_spotify_property("Metadata")
    artist = metadata["xesam:artist"][0]
    title = metadata["xesam:title"]
    return (artist, title)


def show_status():
    artist, title = get_song()
    print(f"{artist} - {title}")


def show_status_short():
    artist, title = get_song()
    artist = artist[:15] + (artist[15:] and "...")
    title = title[:10] + (title[10:] and "...")
    print(f"{artist} - {title}")


def show_song():
    _, title = get_song()
    print(f"{title}")


def show_song_short():
    _, title = get_song()
    title = title[:10] + (title[10:] and "...")
    print(f"{title}")


# Normalize unicode string for a better possibility
# of finding records in azlyrics
def normalize(string):
    return str(ud.normalize("NFKD", string).encode("ASCII", "ignore"), "ASCII")


def get_lyrics_az(artist, song_title):
    artist = normalize(artist.lower())
    song_title = normalize(song_title.lower())

    url = "http://azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"
    url = url.replace(" ", "")

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, "html.parser")
        lyrics_tags = soup.find_all("div", attrs={"class": None, "id": None})
        lyrics = [tag.getText() for tag in lyrics_tags]

        return "".join(lyrics)
    except Exception:
        token = os.environ.get(TOKEN_ENV_VAR)

        if token is not None:
            # Get lyrics from genius
            genius = lg.Genius(token)
            song = genius.search_song(song_title, artist)

            return f"\n{song.lyrics}\n" if song is not None else NO_LYRICS_STR
        else:
            return NO_LYRICS_STR


def get_lyrics():
    try:
        artist, title = get_song()
        return lyricwikia.get_lyrics(artist, title)
    except BaseException:
        return get_lyrics_az(artist, title)


def show_lyrics():
    lyrics = get_lyrics()
    print(lyrics)


def export_lyrics():
    ret = get_lyrics()

    if ret != NO_LYRICS_STR:
        artist, title = get_song()
        path = os.path.join(expanduser("~"), "Lyrics")

        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(path, f"{artist}_{title}.txt")

        with open(path, "w") as f:
            f.write(ret)

        print(f"Saved {path}")
    else:
        print(ret)


def show_artist():
    artist, _ = get_song()
    print(f"{artist}")


def show_artist_short():
    artist, _ = get_song()
    artist = artist[:15] + (artist[15:] and "...")
    print(f"{artist}")


def show_playback_status():
    playback_status = get_spotify_property("PlaybackStatus")
    print({"Playing": "▶", "Paused": "▮▮", "Stopped": "■"}[playback_status])


def show_album():
    metadata = get_spotify_property("Metadata")
    album = metadata["xesam:album"]
    print(f"{album}")


def show_art_url():
    metadata = get_spotify_property("Metadata")
    print("%s" % metadata["mpris:artUrl"])


def get_spotify_property(spotify_property):
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.%s" % client, "/org/mpris/MediaPlayer2"
        )
        spotify_properties = dbus.Interface(
            spotify_bus, "org.freedesktop.DBus.Properties"
        )

        prop = "org.mpris.MediaPlayer2.Player"

        return spotify_properties.Get(prop, spotify_property)
    except BaseException:
        sys.stderr.write(SPOTIFY_OFF_STR)
        sys.exit(1)


def perform_spotify_action(spotify_command):
    Popen(
        'dbus-send --print-reply --dest=org.mpris.MediaPlayer2."%s" ' % client
        + '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player."%s"'
        % spotify_command,
        shell=True,
        stdout=PIPE,
    )


def spotify_is_running():
    return "spotify" in (p.name().lower() for p in psutil.process_iter())


if __name__ == "__main__":
    main()
