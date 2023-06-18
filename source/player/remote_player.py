import typing
from ..configuration import Configuration
from .abstract_player import AbstractPlayer


class RemotePlayer(AbstractPlayer):

    def __init__(self, _id: 'int', ready: 'bool' = False):
        super().__init__(_id)
        self.ready = ready

    def action(self, engine: 'Engine', events: typing.List['pygame.event.Event']) -> 'bool':
        data = engine.wait_from_network()

        if data is None:
            return False
        
        # Check if a barrier was placed
        if data["number_of_barriers_placed"] > self.number_of_barriers_placed:
            self.install(data["barrier.x"], data["barrier.y"], data["barrier.direction"], engine.board)

        # Check if the player has moved
        if data["player.x"] != self.x or data["player.y"] != self.y:
            self.move(data["player.x"], data["player.y"], engine.board)

        return True

    def is_ready(self) -> 'bool':
        return self.ready


AbstractPlayer.PLAYERS[Configuration.PLAYER_TYPES[1]] = RemotePlayer
