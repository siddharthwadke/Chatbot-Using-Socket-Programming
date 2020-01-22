import socket
import select
import errno

HEAD_LEN = 10
#IP = "127.0.0.1"
IP = input("Please enter Host IP address:")
PORT = 5432
usr = input("Please enter your Username: ")
clsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clsoc.connect((IP, PORT))
clsoc.setblocking(False)
usrnme = usr.encode('utf-8')
usrnme_header = f"{len(usrnme):<{HEAD_LEN}}".encode('utf-8')
clsoc.send(usrnme_header + usrnme)

while True:
    data = input(f'{usr} => ')
    if data:
        data = data.encode('utf-8')
        data_header = f"{len(data):<{HEAD_LEN}}".encode('utf-8')
        clsoc.send(data_header + data)

    try:
        while True:
            usrnme_header = clsoc.recv(HEAD_LEN)
            if not len(usrnme_header):
                print('server closed')
                sys.exit()
            usrnme_length = int(usrnme_header.decode('utf-8').strip())
            usrnme = clsoc.recv(usrnme_length).decode('utf-8')
            data_header = clsoc.recv(HEAD_LEN)
            data_length = int(data_header.decode('utf-8').strip())
            data = clsoc.recv(data_length).decode('utf-8')
            print(f'{usrnme} => {data}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Found error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Found error: '.format(str(e)))
        sys.exit()
