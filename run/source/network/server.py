import pickle
import socket
import sys
import threading
import typing
from ..player import RemotePlayer


class Server(threading.Thread):

    class ClientHandler(threading.Thread):
            
        def __init__(self, socket: 'socket.socket', player_id: 'int', server: 'Server'):
            super().__init__()
            self.socket = socket
            self.player_id = player_id
            self.server = server

        def receive_from_client(self) -> typing.Dict[str, typing.Any]:
            size = int.from_bytes(self.socket.recv(4), byteorder="big")
            data = pickle.loads(self.socket.recv(size))
            return data

        def run(self):
            # Send parameters to client
            parameters = self.server._build_parameters(self.player_id)

            self.send_to_client(parameters)

            # Redirect data from client to other clients
            while True:
                data = self.receive_from_client()

                if data is None:
                    break
                for connection in self.server.connections.values():
                    if connection != self:
                        connection.send_to_client(data)
                with self.server.lock:
                    self.server.last_data = data

        def send_to_client(self, data: typing.Any):
            data_to_bytes = pickle.dumps(data)
            size_to_bytes = len(data_to_bytes).to_bytes(4, byteorder="big")

            self.socket.sendall(size_to_bytes + data_to_bytes)

    def __init__(self, address: 'str', port: 'int', engine: 'Engine'):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.engine = engine
        self.connections: typing.Dict['int', 'socket.socket'] = {}

        self.lock = threading.Lock()
        self.last_data = None

        self.socket.bind((address, port))

    def _build_parameters(self, player_id: 'str') -> typing.Dict[str, typing.Any]:
        return {
            "player_id": player_id,
            "board_dimension": self.engine.board_dimension,
            "number_of_barriers": self.engine.number_of_barriers,
            "number_of_players": self.engine.number_of_players,
        }

    def run(self):
        index = 0
        remote_players = [player for player in self.engine.players if isinstance(player, RemotePlayer)]
        max_connections = len(remote_players)

        print("[SERVER] >>> Start server, wait for clients...")
        self.socket.listen(max_connections)
        while index < max_connections:
            connection, address = self.socket.accept()

            print(f"[SERVER]  - Client connected from {address}, played.id = {remote_players[index].id}.")
            self.connections[remote_players[index].id] = Server.ClientHandler(connection, remote_players[index].id, self)
            self.engine.players[remote_players[index].id].ready = True
            index += 1
        print("[SERVER] >>> All clients are connected !")

        for connection in self.connections.values():
            connection.start()
        for connection in self.connections.values():
            connection.join()

    def send_to_clients(self, data: typing.Any):
        for _id, connection in self.connections.items():
            connection.send_to_client(data)

    def wait_data(self) -> typing.Dict[str, typing.Any]:
        with self.lock:
            data = self.last_data
            self.last_data = None
        return data
