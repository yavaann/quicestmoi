import socket
from socket import gethostbyname

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (gethostbyname(str(extract_ip())), 6969)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)




while True:
    print('Waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('Connection from', client_address)

        while True:
            data = connection.recv(8096)
            print(data.decode("utf-8"))
            connection.sendall(input(">> ").encode("utf-8"))
            break
    finally:
        connection.close()
