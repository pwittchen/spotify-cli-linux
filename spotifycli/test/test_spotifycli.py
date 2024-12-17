from io import StringIO
from pathlib import Path
from subprocess import PIPE
from unittest import skip
from unittest.mock import patch

import dbus
import dbusmock

from spotifycli.spotifycli import main
from spotifycli.version import __version__


class TestSpotifyCLI(dbusmock.DBusTestCase):
    @classmethod
    def setUpClass(cls):
        cls.start_session_bus()
        cls.dbus_con = cls.get_dbus(system_bus=False)

    def setUp(self):
        self.dbus_spotify_server_mock = self.spawn_server(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2",
            "org.freedesktop.DBus.Properties",
            system_bus=False,
            stdout=PIPE
        )
        self.dbus_spotify_interface_mock = dbus.Interface(
            self.dbus_con.get_object(
                'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2'
            ),
            dbusmock.MOCK_IFACE
        )
        metadata_file = Path(__file__).resolve().parent / 'dbus_metadata_response.py'
        self.dbus_spotify_interface_mock.AddMethod(
            '', 'Get', 'ss', 'v',
            metadata_file.read_text(),
        )
        # TODO: Mock up the controls bus/interface, since I think it is slightly different
        # self.dbus_spotify_interface_mock.AddMethod(
        #     '', 'Play', '', '', ''
        # )

    def tearDown(self):
        self.dbus_spotify_server_mock.stdout.close()
        self.dbus_spotify_server_mock.terminate()
        self.dbus_spotify_server_mock.wait()

    def test_cli_usage(self):
        with patch('sys.argv', ["spotifycli", "--help"]), patch("sys.exit") as mock_exit, patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("usage", buffer.getvalue())
            mock_exit.assert_called_with(0)

    def test_cli_version(self):
        with patch('sys.argv', ["spotifycli", "--version"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn(__version__, buffer.getvalue())

    def test_cli_status(self):
        with patch('sys.argv', ["spotifycli", "--status"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("The Beatles - Yesterday", buffer.getvalue())

    def test_cli_status_position(self):
        with patch('sys.argv', ["spotifycli", "--statusposition"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            output = buffer.getvalue()
            self.assertIn('00:01', output)
            self.assertIn('00:10', output)

    def test_cli_status_short(self):
        with patch('sys.argv', ["spotifycli", "--statusshort"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            output = buffer.getvalue()
            self.assertIn('Beatles', output)
            self.assertIn('Yesterday', output)

    def test_cli_song(self):
        with patch('sys.argv', ["spotifycli", "--song"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("Yesterday", buffer.getvalue())

    def test_cli_song_short(self):
        # TODO: Change to a long song title to check the trimming
        with patch('sys.argv', ["spotifycli", "--songshort"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("Yesterday", buffer.getvalue())

    def test_cli_artist(self):
        with patch('sys.argv', ["spotifycli", "--artist"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("Beatles", buffer.getvalue())

    def test_cli_artist_short(self):
        # TODO: Change to a long artist name to check the trimming
        with patch('sys.argv', ["spotifycli", "--artistshort"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("Beatles", buffer.getvalue())

    def test_cli_album(self):
        with patch('sys.argv', ["spotifycli", "--album"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn("Help!", buffer.getvalue())

    def test_cli_position(self):
        with patch('sys.argv', ["spotifycli", "--position"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            output = buffer.getvalue()
            self.assertIn('00:01', output)
            self.assertIn('00:10', output)

    def test_cli_art_url(self):
        with patch('sys.argv', ["spotifycli", "--arturl"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            self.assertIn('http', buffer.getvalue())

    def test_cli_playback_status(self):
        with patch('sys.argv', ["spotifycli", "--playbackstatus"]), patch('sys.stdout', new_callable=StringIO) as buffer:
            main()
            playback_symbols = ['▶', '▮▮', '■']
            output = buffer.getvalue()
            self.assertTrue(any([x in output for x in playback_symbols]))

    @skip('Lyrics dont seem to be working right now...is it still valid?')
    def test_cli_lyrics(self):
        with patch('sys.argv', ["spotifycli", "--lyrics"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_play(self):
        with patch('sys.argv', ["spotifycli", "--play"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_pause(self):
        with patch('sys.argv', ["spotifycli", "--pause"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_play_pause(self):
        with patch('sys.argv', ["spotifycli", "--playpause"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_next(self):
        with patch('sys.argv', ["spotifycli", "--next"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_prev(self):
        with patch('sys.argv', ["spotifycli", "--prev"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_songuri(self):
        with patch('sys.argv', ["spotifycli", "--songuri"]):
            main()

    @skip('TODO: Need to mock up the spotify_action dbus interface')
    def test_cli_listuri(self):
        with patch('sys.argv', ["spotifycli", "--listuri"]):
            main()
