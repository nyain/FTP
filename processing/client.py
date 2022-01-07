from processing import Downloads, Uploads

import xmlrpc.client
import os
import time

LISTEN_PORT = 80
LISTEN_HOST = "4952-111-95-183-172.ngrok.io"

proxy = xmlrpc.client.ServerProxy(f'http://{LISTEN_HOST}:{LISTEN_PORT}')

def login(username, password):
    return proxy.login(f'{username},{password}')

def download(username):
    file_array = []
    is_finished = False

    # Mengambil daftar file yang tersedia di folder storage(server)
    files = str(proxy.show_all_files()).split(',')

    # Memilih file yang akan didownload
    while not is_finished:
        print(f'File yang akan didownload adalah : \n {",".join(file_array)}')
        print('Silahkan pilih yang akan didownload')
        for i in range(len(files)):
            print(f'{i + 1}. {files[i]}')
        print(f'{len(files) + 1}. Cukup')
        print(f'{len(files) + 2}. Kembali')
        choice = int(input(f'Masukkan pilihan anda (1-{len(files) + 2}) -> '))

        if choice not in range(len(files) + 3):
            print('Pilihan salah')
            from cli import main
            main(username)

        if choice == len(files) + 1:
            is_finished = True
        if choice == len(files) + 2:
            is_finished = True
            from cli import main
            main(username)
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Downloads(file, username)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)

def upload(username):
    file_array = []
    is_finished = False

    # Mengambil daftar file yang tersedia di folder storage(server)
    files = os.listdir(os.getcwd())

    # Memilih file yang akan diupload
    while not is_finished:
        print(f'File yang akan diupload adalah : \n {",".join(file_array)}')
        print('Silahkan pilih yang akan diupload')
        for i in range(len(files)):
            print(f'{i + 1}. {files[i]}')
        print(f'{len(files) + 1}. Cukup')
        print(f'{len(files) + 2}. Kembali')
        choice = int(input(f'Masukkan pilihan anda (1-{len(files) + 2}) -> '))

        if choice not in range(len(files) + 3):
            print('Pilihan salah')
            from cli import main
            main(username)

        if choice == len(files) + 1:
            is_finished = True
        if choice == len(files) + 2:
            is_finished = True
            from cli import main
            main(username)
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Uploads(file, username)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)
