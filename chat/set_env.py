import os
import click
from termcolor import colored
FILE_PATH = ".env"

def confirm(message:str):
    answer = input(message) 
    while answer not in ["Y", "N"]: 
        answer = input("please answer only with Y or N ")

    return answer

if 'ENV_FILE_LOCATION' not in os.environ:
    answer = confirm(colored(r"Notice, in order to get this server to work, you'll need to addd enviroment variable. Continue? (Y\N)"))
    if answer == "N":
        exit()

os.environ['ENV_FILE_LOCATION'] = FILE_PATH
relative_path = os.path.relpath(os.path.dirname(__file__), FILE_PATH)
if not os.path.exists(relative_path):
    with open(relative_path, "w") as f:
        key =input("Please sign your key")
        while key is "":
            key =input("Please sign you key")
        f.write("JWT_SECRET_KEY = '{}}'".format(key))