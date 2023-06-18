import pygame
import random
import typing
from ..configuration import Configuration
from .abstract_player import AbstractPlayer
from .local_player import LocalPlayer


class AIPlayer(LocalPlayer):

    def action(self, engine: 'Engine', events: typing.List['pygame.event.Event']) -> 'bool':
        if self.number_of_barriers_placed < engine.number_of_barriers and random.random() >= 0.50:
            while True:
                x = random.randint(0, engine.board.width - 1)
                y = random.randint(0, engine.board.height - 1)
                direction = random.choice(["vertical", "horizontal"])
                number_of_barriers_left = engine.number_of_barriers - self.number_of_barriers_placed

                if engine.board.is_possible_installation(x, y, direction, number_of_barriers_left, engine.players) is True:
                    self.install(x, y, direction, engine.board)
                    engine.update_to_network()
                    return True
        else:
            while True:
                x, y = random.choice(AbstractPlayer.MOVES)(self.x, self.y)

                if engine.board.is_possible_move(self.x, self.y, x, y) is True:
                    self.move(x, y, engine.board)
                    engine.update_to_network()
                    return True


AbstractPlayer.PLAYERS[Configuration.PLAYER_TYPES[2]] = AIPlayer
