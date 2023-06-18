import pygame
import typing
from .configuration import Configuration
from .board import Board
from .network import Client, Server


class Engine:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Configuration.TITLE)
        self.surface: 'pygame.Surface'    = pygame.display.set_mode(Configuration.WINDOW_SIZE)
        self.current_view: 'AbstractView' = None

        self.board_dimension: typing.Tuple['int', 'int'] = None
        self.number_of_barriers: 'int'                   = None
        self.number_of_players: 'int'                    = None

        self.board: 'Board'                         = Board()
        self.player_turn: 'int'                     = None
        self.players: typing.List['AbstractPlayer'] = None
        self.game_running: 'bool'                   = False

        self.client: 'Client' = None
        self.server: 'Server' = None

    def initialize_game(self):
        self.game_running = True
        self.player_turn = 0
        self.board.initialize(self.board_dimension)
        for player in self.players:
            player.initialize(self.board)
            self.board.cells[(player.x, player.y)].occupied_by = player.id

    def load_view(self, view: 'AbstractView'):
        self.current_view = view
        
        self.current_view.initialize(self)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.game_running is True:
                if self.players[self.player_turn].action(self, events) is True:
                    if self.players[self.player_turn].has_won() is True:
                        self.players[self.player_turn].score += 1
                        self.game_running = False
                    self.player_turn = (self.player_turn + 1) % self.number_of_players

            if self.current_view is not None:
                self.current_view.run(self, events)
            pygame.display.update()
            pygame.event.clear()
            self.surface.fill(Configuration.BACKGROUND_COLOR)
            pygame.time.wait(1000 // Configuration.FRAME_PER_SECOND)

    def start_network(self, ip_address: 'str' = None):
        if ip_address is not None:
            self.client = Client(ip_address, Configuration.SERVER_PORT, self)

            self.client.start()
        else:
            self.server = Server(Configuration.SERVER_IP, Configuration.SERVER_PORT, self)

            self.server.start()

    def stop_network(self):
        if self.client is not None:
            if self.client.is_alive() is True:
                self.client.close()
            self.client = None
        if self.server is not None:
            if self.server.is_alive() is True:
                self.server.close()
            self.server = None

    def update_to_network(self):
        data = {
            "number_of_barriers_placed": self.players[self.player_turn].number_of_barriers_placed,
            "barrier.x": self.players[self.player_turn].last_barrier[0],
            "barrier.y": self.players[self.player_turn].last_barrier[1],
            "barrier.direction": self.players[self.player_turn].last_barrier[2],
            "player.x": self.players[self.player_turn].x,
            "player.y": self.players[self.player_turn].y
        }

        if self.client is not None:
            self.client.send_to_server(data)
        if self.server is not None:
            self.server.send_to_clients(data)

    def wait_from_network(self):
        if self.client is not None:
            return self.client.wait_data()
        if self.server is not None:
            return self.server.wait_data()
