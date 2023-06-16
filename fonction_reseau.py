import threading
import socket
import pickle
import time


def envoyer_parametre_client_vers_server(joueurs, parametre):
    parametre_bytes = pickle.dumps(parametre)
    data_size = len(parametre_bytes).to_bytes(4, byteorder='big')
    joueurs.sendall(data_size + parametre_bytes)
    print('-----------------------------------parametre envoyé au server-----------------------------------')

def envoyer_parametre_server_vers_client(connexion, parametre,id_client):
        parametre['id_client'] = id_client
        parametre_bytes = pickle.dumps(parametre)
        data_size = len(parametre_bytes).to_bytes(4, byteorder='big')
        connexion.sendall(data_size + parametre_bytes)
        print('-----------------------------------parametre envoyé au client-----------------------------------')

def recevoir_parametre_server(connexion):
    try:
        data_size = int.from_bytes(connexion.recv(4), byteorder='big')
        data = pickle.loads(connexion.recv(data_size))
        print('-----------------------------------parametre reçu du client-----------------------------------')
    except Exception as e:
        print(f"Une erreur s'est produite lors de la réception des données : {e}")
        return False
    if not data:
        return False
    return data

def recevoir_parametre_client(connexion):
    try:
        data_size = int.from_bytes(connexion.recv(4), byteorder='big')
        data = pickle.loads(connexion.recv(data_size))
        print('-----------------------------------parametre reçu du server-----------------------------------')
    except Exception as e:
        print(f"Une erreur s'est produite lors de la réception des données : {e}")
        return False
    if not data:
        return False
    return data

def join_game(addr):
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((str(addr), 12800))
    print("Connexion établie avec le serveur sur le port {}".format(12800))
    return connexion_avec_serveur


class ThreadforServer(threading.Thread):
    def __init__(self, conn, address, client_conns):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.client_conns = client_conns
        self.data = None
        self.lock = threading.Lock()

    def recevoir_tableau_jeu_server(self):
        try:
            while True:
                data = self.conn.recv(4096)
                if not data:
                    break
                self.lock.acquire()
                self.data = pickle.loads(data)
                print(self.data)
                self.lock.release()
                print('-----------------------------------tableau reçu du client-----------------------------------')
                self.envoyer_tableau_jeu_server()
        except Exception as e:
            print(f"Une erreur s'est produite lors de la réception des données : {e}")
            return False
        return True

    def envoyer_tableau_jeu_server(self):
        try:
            data = pickle.dumps(self.data)
            for client_conn in self.client_conns:
                client_conn.sendall(data)
            print('-----------------------------------tableau envoyé au client-----------------------------------')
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'envoi des données : {e}")
            return False
        return True

    def run(self):
        while True:
            if not self.recevoir_tableau_jeu_server():
                break
            self.envoyer_tableau_jeu_server()


def envoyer_tableau_jeu(conn, board, walls, player_in_game):
    data = {"board": board, "walls": walls,"player_in_game": player_in_game}
    try:
        data_bytes = pickle.dumps(data)
        conn.sendall(data_bytes)
        print('Tableau envoyé au serveur')
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'envoi des données au serveur : {e}")


def recevoir_tableau_jeu(conn):
    try:
        data = conn.recv(4096)
        if not data:
            return False
        data = pickle.loads(data)
        print('Tableau reçu du serveur')
        return data
    except Exception as e:
        print(f"Une erreur s'est produite lors de la réception des données du serveur : {e}")
        return False

