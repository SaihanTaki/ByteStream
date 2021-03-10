import socket
import zlib
import tqdm
import sys
import os


HOST = "127.0.0.1"
PORT = 5050
ADDRESS = (HOST, PORT)

BUFFER_SIZE = 4096
FORMAT = "utf-8"
SEPARATOR = "/"

family = socket.AF_INET  # Ipv4
protocol = socket.SOCK_STREAM  # Tcp

status = str(sys.argv[1])
filename = str(sys.argv[2])

if os.path.exists(filename) and status == 'send':
    filesize = os.path.getsize(filename)
elif status == 'recv':
    new_filename = filename
else:
    pass


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[+] Connecting to {HOST}:{PORT}")
client.connect(ADDRESS)
print("[+] Connected.")


def progress_info(filename, filesize, status):
    if status == 'send':
        status = 'Sending'
    if status == 'recv':
        status = 'Receiving'

    progress = tqdm.tqdm(range(
        filesize), f"{status} {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    return progress


def recv_info(connection):
    received = connection.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    return filename, filesize


def send_info(client, filename, filesize):
    client.send(f"{filename}{SEPARATOR}{filesize}".encode())
    return None


def send_file(client, filename, progress):
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            compressed_data = zlib.compress(bytes_read, 2)
            client.sendall(compressed_data)
            progress.update(len(bytes_read))
    return None


def recv_file(client, filename, progress):
    with open(filename, "wb") as f:
        while True:
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            bytes_read = zlib.decompress(bytes_read)
            f.write(bytes_read)
            progress.update(len(bytes_read))
    return None


if status == 'recv':
    filename, filesize = recv_info(client)
    progress = progress_info(filename, filesize, status)
    recv_file(client, new_filename, progress)
    client.close()

elif status == 'send':
    send_info(client, filename, filesize)
    progress = progress_info(filename, filesize, status)
    send_file(client, filename, progress)
    client.close()
