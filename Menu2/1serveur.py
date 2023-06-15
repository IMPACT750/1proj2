import socket
import threading

class ThreadforClient(threading.Thread):
    def __init__(self, conn, address, lock, client_conns):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.lock = lock
        self.client_conns = client_conns

    def envoie_des_donnees(self):
        message = f"{player1.x},{player1.y},{player2.x},{player2.y}"
        with self.lock:
            for client_conn in self.client_conns:
                client_conn.sendall(message.encode('utf-8'))
        print(message, "à tous les clients")

    def recevoir_des_donnees(self):
        data = self.conn.recv(1024).decode()
        if data:
            coords = data.split(',')
            print(coords)
            x1 = int(coords[0])
            y1 = int(coords[1])
            x2 = int(coords[2])
            y2 = int(coords[3])
            player1.x = x1
            player1.y = y1
            player2.x = x2
            if y2 > 8:
                player2.y = 8
            else:
                player2.y = y2
            return True
        else:
            return False

    def run(self):
        while True:
            if not self.recevoir_des_donnees():
                break
            self.envoie_des_donnees()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_walls = 10

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1


player1 = Player(4, 0)
player2 = Player(4, 8)

host, port = ('', 5566)
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((host, port))
socket_server.listen()
client_conns = []
lock = threading.Lock()

while True:
    conn, address = socket_server.accept()
    client_conns.append(conn)
    print(f"Client connecté {address}")
    if len(client_conns) == 2:
        threads = []
        for client_conn in client_conns:
            thread = ThreadforClient(client_conn, address, lock, client_conns)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        client_conns.clear()

socket_server.close()
