from os import system

files = [
    "spotifycli/spotifycli.py",
    "spotifycli/version.py",
    "spotifycli/__main__.py",
    "spotifycli/__init__.py",
    "setup.py",
]


def check_format():
    for i in files:
        system(f"pycodestyle --show-source --show-pep8 --format=default {i}")


if __name__ == "__main__":
    check_format()
