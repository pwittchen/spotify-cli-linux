from os import system

files = [
    "spotifycli/spotifycli.py",
    "spotifycli/version.py",
    "spotifycli/__main__.py",
    "spotifycli/__init__.py",
    "setup.py"
]


def format():
    for i in files:
        system(f"autopep8 --in-place --aggressive {i}")


if __name__ == "__main__":
    format()
