import threading
import socket
import pickle
import time


def envoyer_parametre_client_vers_server(joueurs, parametre):
    parametre_bytes = pickle.dumps(parametre)
    data_size = len(parametre_bytes).to_bytes(4, byteorder='big')
    joueurs.sendall(data_size + parametre_bytes)
    print('-----------------------------------parametre envoyé au server-----------------------------------')

def envoyer_parametre_server_vers_client(connection, parametre):
        parametre_bytes = pickle.dumps(parametre)
        data_size = len(parametre_bytes).to_bytes(4, byteorder='big')
        connection.sendall(data_size + parametre_bytes)
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
        self.lock = threading.Lock()
        self.client_conns = client_conns
        self.data = []

    def recevoir_tableau_jeu(self):
        try:
            self.data = pickle.loads(self.conn.recv(1024))
        except Exception as e:
            print(f"Une erreur s'est produite lors de la réception des données : {e}")
            return False
        if not self.data:
            return False
        with self.lock:
            for client_conn in self.client_conns:
                if client_conn != self.conn:
                    self.envoyer_tableau_jeu()
        return True

    def envoyer_tableau_jeu(self):
        try:
            self.conn.sendall(pickle.dumps(self.data))
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'envoi des données : {e}")
            return False
        return True


    def run(self):
        while True:
            if not self.recevoir_tableau_jeu():
                break
            self.envoyer_tableau_jeu()



def envoyer_tableau_jeu(conn,board,walls):
    data = {"tableau_joueur": board, "tableau_wall": walls}
    data_bytes = pickle.dumps(data)
    data_size = len(data_bytes).to_bytes(4, byteorder='big')
    conn.sendall(data_size + data_bytes)


class ThreadforClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.lock = threading.Lock()
        self.data = []


    def recevoir_tableau_jeu(self):
        with self.lock:
            try:
                self.data = pickle.loads(self.conn.recv(1024))
                return self.data
            except Exception as e:
                print(f"Une erreur s'est produite lors de la réception des données : {e}")
                return False
            if not self.data:
                return False
        return 

    
    def run(self):
        while True:
            if self.recevoir_tableau_jeu():
                time.sleep(0.1)
            else:
                break

