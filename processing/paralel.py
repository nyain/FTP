import threading
import xmlrpc.client
import os

LISTEN_PORT = 80
LISTEN_HOST = "4952-111-95-183-172.ngrok.io"

proxy = xmlrpc.client.ServerProxy(f'http://{LISTEN_HOST}:{LISTEN_PORT}')
lock = threading.Lock()

class Downloads(threading.Thread):
    def __init__(self, file, username):
        threading.Thread.__init__(self)
        self.file = file
        self.username = username

    def run(self):
        if os.path.exists(f'downloaded/{self.file}'):
            print("File already exist !!")
        else:
            # Write file dari server ke direktori downloaded
            with lock:
                with open(f'downloaded/{self.file}', 'wb') as writer:
                    data = proxy.download(self.file, self.username).data
                    writer.write(data)

class Uploads(threading.Thread):
    def __init__(self, file, username):
        threading.Thread.__init__(self)
        self.file = file
        self.username = username

    def run(self):
        if os.path.exists(f'storage/{self.file}'):
            print("File already exist !!")
        else:
            # Write file dar client ke direktori storage
            with lock:
                with open(self.file, 'rb') as data:
                    raw_data = xmlrpc.client.Binary(data.read())
                    is_uploaded = proxy.upload(raw_data, self.file, self.username)
                    if not is_uploaded:
                        print("File already exists !!")
