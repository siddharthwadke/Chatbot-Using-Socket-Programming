import socket
import select
HEAD_LEN = 10
IP = input("Enter Host IP address:")
#IP = "127.0.0.1" #statc ip
PORT = 5432
serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_soc.bind((IP, PORT))
serv_soc.listen()
soc_lst = [serv_soc]
clnt = {}
print(f'Waiting for clients on IP {IP} and Port no. {PORT}')
def recei_data(client_socket):
    try:
        message_header = client_socket.recv(HEAD_LEN)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False
while True:
    rd_sock, _, exp_soc = select.select(soc_lst, [], soc_lst)
    for sock_notif in rd_sock:
        if sock_notif == serv_soc:
            client_socket, cl_addr = serv_soc.accept()
            usr = recei_data(client_socket)
            if usr is False:
                continue
            soc_lst.append(client_socket)
            clnt[client_socket] = usr
            print('New connection established from Client {}:{}, User Connected: {}'.format(*cl_addr, usr['data'].decode('utf-8')))
        else:
            message = recei_data(sock_notif)
            if message is False:
                print('User left chat: {}'.format(clnt[sock_notif]['data'].decode('utf-8')))
                soc_lst.remove(sock_notif)
                del clnt[sock_notif]
                continue
            usr = clnt[sock_notif]
            print(f'Message from {usr["data"].decode("utf-8")} => {message["data"].decode("utf-8")}')
            for client_socket in clnt:
                if client_socket != sock_notif:
                    client_socket.send(usr['header'] + usr['data'] + message['header'] + message['data'])
    for sock_notif in exp_soc:
        soc_lst.remove(sock_notif)
        del clnt[sock_notif]
