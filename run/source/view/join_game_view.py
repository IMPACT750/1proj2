import pygame, pygame_menu
import typing
from ..configuration import Configuration
from .abstract_view import AbstractView


class JoinGameView(AbstractView):

    def initialize(self, engine: 'Engine'):
        self.menu = pygame_menu.Menu(
            Configuration.TITLE,
            *Configuration.WINDOW_SIZE,
            theme=pygame_menu.themes.Theme(
                background_color="black",
                title_background_color="black",
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font_color="white"))

        # IP address input
        ip_address = self.menu.add.text_input("IP address : ", default="localhost")

        # Navigation buttons
        self.menu.add.button("Join", (lambda: engine.load_view(AbstractView.make_view("waiting_room", ip_address=ip_address.get_value()))))
        self.menu.add.button("Back", (lambda: engine.load_view(AbstractView.make_view("home"))))

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(engine.surface)


AbstractView.VIEWS["join_game"] = JoinGameView
