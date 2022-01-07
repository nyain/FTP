import os

from processing import login
from getpass import getpass

def login_prompt():
    repeat = True
    while repeat:
        os.system('cls' if os.name == 'nt' else 'clear')
        username = str(input("Username: "))
        password = getpass()
        valid = login(username, password)
        if valid:
            from cli import main
            main(username)
        else:
            print("Username/password salah")
            exit(0)
