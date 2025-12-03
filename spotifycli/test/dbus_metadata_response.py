if args[1] == 'Metadata':
    ret = {
        'xesam:artist': ['', 'The Beatles'],
        'xesam:title': ['', 'Yesterday'],
        'xesam:album': ['', 'Help!'],
        'mpris:length': ['', '10000000'],
        'mpris:artUrl': ['', 'https://github.com/pwittchen/spotify-cli-linux'],
    }
elif args[1] == 'PlaybackStatus':
    ret = 'Playing'
elif args[1] == 'Position':
    ret = 1000000
else:
    ret = args
