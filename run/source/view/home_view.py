import pygame, pygame_menu
import typing
from ..configuration import Configuration
from .abstract_view import AbstractView


class HomeView(AbstractView):

    def initialize(self, engine: 'Engine'):
        engine.game_running = False

        self.menu = pygame_menu.Menu(
            Configuration.TITLE,
            *Configuration.WINDOW_SIZE,
            theme=pygame_menu.themes.Theme(
                background_color="black",
                title_background_color="black",
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font_color="white"))

        # Navigation buttons
        self.menu.add.button("Create a game", (lambda: engine.load_view(AbstractView.make_view("game_configuration"))))
        self.menu.add.button("Join a game", (lambda: engine.load_view(AbstractView.make_view("join_game"))))
        self.menu.add.button("Exit", pygame_menu.events.EXIT)

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(engine.surface)


AbstractView.VIEWS["home"] = HomeView
