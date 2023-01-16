import socket
import threading

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

pseudo = input("Pseudo : ")


class srv():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (input("> "), 6969)
        print('Connecting to {} port {}'.format(*self.server_address))
        self.sock.connect(self.server_address)
    def recevoir(self):
        while True:
            try:
                data = self.sock.recv(8096)
                print(data.decode("utf-8"))
            finally:
                None
    def envoyer(self):
        while True:
            while True:
                message = input(">> ")
                if message == "":
                    break
                message = pseudo+" : "+message+"\n"
                self.sock.sendall(message.encode("utf-8"))

serv = srv()

t1 = threading.Thread(target=serv.recevoir)
t2 = threading.Thread(target=serv.envoyer)
t1.start()
t2.start()
t1.join()
t2.join()