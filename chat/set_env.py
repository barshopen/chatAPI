import os
import pathlib
FILE_PATH = ".env"

path = os.path.join(pathlib.Path(__file__).parent.absolute(), FILE_PATH)
print(path)
os.environ['ENV_FILE_LOCATION'] = path
if not os.path.exists(path):
    with open(path, "w+") as f:
        key = input("Please sign your key")
        while key is "":
            key =input("Please sign you key")
        f.write("\nJWT_SECRET_KEY = '{}}'".format(key))