import os
import click
from termcolor import colored
FILE_PATH = ".env"

os.environ['ENV_FILE_LOCATION'] = FILE_PATH
relative_path = os.path.relpath(os.path.dirname(__file__), FILE_PATH)
if not os.path.exists(relative_path):
    with open(relative_path, "w") as f:
        key = input("Please sign your key")
        while key is "":
            key =input("Please sign you key")
        f.write("JWT_SECRET_KEY = '{}}'".format(key))