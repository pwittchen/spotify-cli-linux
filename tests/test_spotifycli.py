"""Tests for spotifycli.spotifycli."""

import spotifycli.spotifycli as spotifycli


def test_show_playback_status_unknown_prints_raw_status(monkeypatch, capsys):
    """An unrecognized playback status must not raise KeyError."""
    monkeypatch.setattr(spotifycli, "get_spotify_property", lambda name: "Rewinding")

    spotifycli.show_playback_status()

    out, _ = capsys.readouterr()
    assert out.strip() == "Rewinding"


def test_show_playback_status_known_symbols(monkeypatch, capsys):
    """Known statuses keep their existing symbols."""
    for status, symbol in (("Playing", "\u25b6"), ("Paused", "\u25ae\u25ae"), ("Stopped", "\u25a0")):
        monkeypatch.setattr(spotifycli, "get_spotify_property", lambda name: status)
        spotifycli.show_playback_status()
        out, _ = capsys.readouterr()
        assert out.strip() == symbol
