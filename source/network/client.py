import pickle
import socket
import sys
import threading
import typing
from ..player import LocalPlayer, RemotePlayer
from ..view import AbstractView


class Client(threading.Thread):

    def __init__(self, address: 'str', port: 'int', engine: 'Engine'):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.engine = engine

        self.lock = threading.Lock()
        self.last_data = None

    def receive_from_server(self) -> typing.Dict[str, typing.Any]:
        size = int.from_bytes(self.socket.recv(4), byteorder="big")
        data = pickle.loads(self.socket.recv(size))
        return data

    def run(self):
        # Connect to server
        self.socket.connect((self.address, self.port))
        print(f"[CLIENT] >>> Connection established with the server on port {self.port}.")

        # Receive parameters
        parameters = self.receive_from_server()

        self.engine.board_dimension = parameters["board_dimension"]
        self.engine.number_of_barriers = parameters["number_of_barriers"]
        self.engine.number_of_players = parameters["number_of_players"]
        self.engine.players = [None for _ in range(self.engine.number_of_players)]
        for _id in range(self.engine.number_of_players):
            if _id == parameters["player_id"]:
                self.engine.players[_id] = LocalPlayer(_id)
            else:
                self.engine.players[_id] = RemotePlayer(_id, True)
        self.engine.load_view(AbstractView.make_view("game"))

        # Receive data from server
        while True:
            data = self.receive_from_server()

            if data is None:
                break
            with self.lock:
                self.last_data = data

    def send_to_server(self, data: typing.Any):
        data_to_bytes = pickle.dumps(data)
        size_to_bytes = len(data_to_bytes).to_bytes(4, byteorder="big")

        self.socket.sendall(size_to_bytes + data_to_bytes)

    def wait_data(self) -> typing.Dict[str, typing.Any]:
        with self.lock:
            data = self.last_data
            self.last_data = None
        return data
