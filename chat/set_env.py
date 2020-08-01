import os
import click
from termcolor import colored
FILE_PATH = ".env"

relative_path = os.path.join(os.path.relpath(os.path.dirname(__file__), FILE_PATH), FILE_PATH)
os.environ['ENV_FILE_LOCATION'] = relative_path
print(relative_path)
if not os.path.exists(relative_path):
    with open(relative_path, "w+") as f:
        key = input("Please sign your key")
        while key is "":
            key =input("Please sign you key")
        f.write("\nJWT_SECRET_KEY = '{}}'".format(key))