from xmlrpc.server import SimpleXMLRPCServer
from tabulate import tabulate

import xmlrpc.client
import os
import pymysql

LISTEN_PORT = 8080
LISTEN_HOST = "127.0.0.1"

connection = pymysql.connect(db="ftp", user="root", password="")

def perform_update(column_name, username):
    # Execute cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f'SELECT id, {column_name} FROM ftp WHERE username=%s', username)

    # Convert cursor to dictionary
    client = cursor.fetchone()
    updated_data = client[column_name] + 1
    update_cursor = connection.cursor()

    # Update data
    update_cursor.execute(f'UPDATE ftp SET {column_name} = %s WHERE id = %s', (updated_data, client['id']))

    # Close cursor
    cursor.close()
    update_cursor.close()

    # Commit change
    connection.commit()

    clients_activity()

def login(credentials):
    username, password = credentials.split(',')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT username, password FROM ftp WHERE username=%s', username)
    client = cursor.fetchone()
    cursor.close()
    return True if client and client['password'] == password else False

def download(file_name, username):
    if os.path.exists(f'storage/{file_name}'):
        perform_update('activity_download', username)
        with open(f'storage/{file_name}', 'rb') as file:
            return xmlrpc.client.Binary(file.read())
    else:
        print("Error: File not found")
        return xmlrpc.client.Binary(b'Error: File not found !!')

def upload(file_data, filename, username):
    if not os.path.exists(f'storage/{filename}'):
        with open(f"storage/{filename}", 'wb') as file:
            file.write(file_data.data)

        perform_update('activity_upload', username)
        return True
    else:
        print('Error: File already exists')
        return False

def show_all_files():
    files = ','.join(os.listdir('storage')).encode()
    return xmlrpc.client.Binary(bytes(files))

def clients_activity():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT username, activity_upload, activity_download FROM ftp;')
    clients = cursor.fetchall()
    header = clients[0].keys()
    rows = [x.values() for x in clients]
    print(tabulate(rows, header))
    return clients

# Create server
server = SimpleXMLRPCServer((LISTEN_HOST, LISTEN_PORT))

# Register function to RPC
server.register_function(download, 'download')
server.register_function(upload, 'upload')
server.register_function(show_all_files, 'show_all_files')
server.register_function(login, 'login')
server.register_function(clients_activity, 'clients_activity')

def loop():
    #exception handling saat terminate menggunkan ctrl+c
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
        print("Program dihentikan..")
        pass

print(f"Listen on {LISTEN_HOST}:{LISTEN_PORT}")
loop()
