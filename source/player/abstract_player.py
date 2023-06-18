import pygame
import typing


class AbstractPlayer:

    MOVES = (
        lambda x, y: (x, y - 1),
        lambda x, y: (x, y + 1),
        lambda x, y: (x - 1, y),
        lambda x, y: (x + 1, y)
    )
    PLAYERS = {}

    @staticmethod
    def make_player(name: 'str', _id: 'int') -> 'AbstractPlayer':
        return AbstractPlayer.PLAYERS[name](_id)

    def __init__(self, _id: 'int'):
        self.id = _id
        self.number_of_barriers_placed: 'int' = None
        self.x: 'int' = None
        self.y: 'int' = None
        self.targets: typing.List['int'] = []
        self.score: 'int' = 0
        self.last_barrier: typing.Tuple['int', 'int', 'str'] = None

    def action(self, engine: 'Engine', events: typing.List['pygame.event.Event']) -> 'bool':
        raise NotImplementedError()

    def has_won(self) -> 'bool':
        return (self.x, self.y) in self.targets

    def initialize(self, board: 'Board'):
        self.number_of_barriers_placed = 0
        self.x = {2: 0, 3: board.width - 1}.get(self.id, board.width // 2)
        self.y = {0: 0, 1: board.height - 1}.get(self.id, board.height // 2)
        self.last_barrier = (None, None, None)

        self.targets.clear()
        for x, y in zip(range(board.width), range(board.height)):
            if self.x == board.width // 2:
                self.targets.append((x, abs(self.y - (board.height - 1))))
            else:
                self.targets.append((abs(self.x - (board.width - 1)), y))

    def install(self, x: 'int', y: 'int', direction: 'str', board: 'Board'):
        board.barriers[(x, y, direction)].installed_by = self.id
        self.number_of_barriers_placed += 1
        self.last_barrier = (x, y, direction)

    def is_ready(self) -> 'bool':
        raise NotImplementedError()

    def move(self, x: 'int', y: 'int', board: 'Board'):
        board.cells[(self.x, self.y)].occupied_by = None
        self.x = x
        self.y = y
        board.cells[(self.x, self.y)].occupied_by = self.id
