import pygame, pygame_menu
import typing
from ..configuration import Configuration
from .abstract_view import AbstractView


class GameConfigurationView(AbstractView):

    def initialize(self, engine: 'Engine'):
        def set_board_dimension(_, index: int):
            engine.board_dimension = Configuration.BOARD_DIMENSIONS[index]
        def set_number_of_players(_, index: int):
            engine.number_of_players = Configuration.NUMBER_OF_PLAYERS[index]
        def set_number_of_barriers(_, index: int):
            engine.number_of_barriers = Configuration.NUMBER_OF_BARRIERS[index]
        self.menu = pygame_menu.Menu(
            Configuration.TITLE,
            *Configuration.WINDOW_SIZE,
            theme=pygame_menu.themes.Theme(
                background_color="black",
                title_background_color="black",
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font_color="white"))

        # Board dimension
        set_board_dimension(None, 0) # Set default board dimension
        self.menu.add.selector(
            "Board dimension : ",
            [(f"{x[0]}x{x[1]}", index) for index, x in enumerate(Configuration.BOARD_DIMENSIONS)],
            onchange=set_board_dimension,
            font_size=28)

        # Number of players
        set_number_of_players(None, 0) # Set default number of players
        self.menu.add.selector(
            "Number of players : ",
            [(f"{x}", index) for index, x in enumerate(Configuration.NUMBER_OF_PLAYERS)],
            onchange=set_number_of_players,
            font_size=28)

        # Number of barriers
        set_number_of_barriers(None, 0) # Set default number of barriers
        self.menu.add.selector(
            "Number of barriers per player : ",
            [(f"{x}", index) for index, x in enumerate(Configuration.NUMBER_OF_BARRIERS)],
            onchange=set_number_of_barriers,
            font_size=28)

        # Navigation buttons
        self.menu.add.button("Next", (lambda: engine.load_view(AbstractView.make_view("players_configuration"))))
        self.menu.add.button("Back", (lambda: engine.load_view(AbstractView.make_view("home"))))

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(engine.surface)


AbstractView.VIEWS["game_configuration"] = GameConfigurationView
