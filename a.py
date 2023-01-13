import socket

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


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (extract_ip(), 6969)
    print('Connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Envoi de données
        message = input(">> ")
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(8096)
        print(data.decode("utf-8"))



    finally:
        print('Closing socket')
        None
