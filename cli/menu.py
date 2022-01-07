from processing import upload, download

import os

def main(username):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('1. Upload')
    print('2. Download')
    print('3. Exit')
    choice = int(input('Input: '))
    if choice == 1:
        upload(username)
        main(username)
    elif choice == 2:
        download(username)
        main(username)
    elif choice == 3:
        exit(0)
    else:
        exit(0)
