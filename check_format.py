from subprocess import call
import sys

files = [
    "spotifycli/spotifycli.py",
    "spotifycli/version.py",
    "spotifycli/__main__.py",
    "spotifycli/__init__.py",
    "setup.py",
]


def check_format():
    any_failed = False
    for i in files:
        exit_code = call(["pycodestyle", "--show-source", "--show-pep8", "--format=default", i])
        any_failed |= True if exit_code == 1 else False
    return any_failed


if __name__ == "__main__":
    sys.exit(check_format())
