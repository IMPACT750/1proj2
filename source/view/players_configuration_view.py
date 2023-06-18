import pygame, pygame_menu
import typing
from ..configuration import Configuration
from ..player import AbstractPlayer
from .abstract_view import AbstractView


class PlayersConfigurationView(AbstractView):

    def initialize(self, engine: 'Engine'):
        def set_player(_, index: int, _id: int):
            engine.players[_id] = AbstractPlayer.make_player(Configuration.PLAYER_TYPES[index], _id)
        self.menu = pygame_menu.Menu(
            Configuration.TITLE,
            *Configuration.WINDOW_SIZE,
            theme=pygame_menu.themes.Theme(
                background_color="black",
                title_background_color="black",
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font_color="white"))

        # Player types
        engine.players = [None for _ in range(engine.number_of_players)]

        for _id in range(engine.number_of_players):
            set_player(None, 0, _id) # Set default player type
        self.menu.add.label(f"Player 1 : <{Configuration.PLAYER_TYPES[0]}> (you)", font_size=28)
        for _id in range(1, engine.number_of_players):
            self.menu.add.selector(
                f"Player {_id + 1} : ",
                [(f"{x}", index, _id) for index, x in enumerate(Configuration.PLAYER_TYPES)],
                onchange=set_player,
                font_size=28)

        # Navigation buttons
        self.menu.add.button("Create", (lambda: engine.load_view(AbstractView.make_view("waiting_room"))))
        self.menu.add.button("Back", (lambda: engine.load_view(AbstractView.make_view("game_configuration"))))

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(engine.surface)


AbstractView.VIEWS["players_configuration"] = PlayersConfigurationView
