import socket
from fonction_reseau import *



host, port = ('', 12800)
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((host, port))
socket_server.listen()
client_conns = []
print(f"Serveur en attente sur le port {port} ...")
print(f"Adresse IP du serveur : {socket.gethostbyname(socket.gethostname())}")
parametre = {}
id_client = 1 

while True:
    conn, address = socket_server.accept()
    client_conns.append(conn)
    print(f"Client connecté {address}")
    if len(parametre) == 0:
        parametre = recevoir_parametre_server(conn)
    envoyer_parametre_server_vers_client(conn, parametre, id_client)
    id_client += 1
    if len(client_conns) == parametre['nb_player']:
        break
threads = []
for client_conn in client_conns:
    thread = ThreadforServer(client_conn, address, client_conns)
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

socket_server.close()
