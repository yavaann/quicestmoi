import socket

# Création d'un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
server_address = ('localhost', 6969)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Envoi de données
    message = input(">> ")
    sock.sendall(message.encode("utf-8"))



finally:
    print('Closing socket')
    sock.close()
