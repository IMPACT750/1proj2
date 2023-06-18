import pygame, pygame_menu
import typing
from ..configuration import Configuration
from ..player import RemotePlayer
from .abstract_view import AbstractView
from .widget import LabelWidget


class WaitingRoomView(AbstractView):

    def initialize(self, engine: 'Engine'):
        self.menu = pygame_menu.Menu(
            Configuration.TITLE,
            *Configuration.WINDOW_SIZE,
            theme=pygame_menu.themes.Theme(
                background_color="black",
                title_background_color="black",
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font_color="white"))

        if "ip_address" in self.parameters:
            ip_address = self.parameters["ip_address"]
            engine.start_network(ip_address)

            # Information label
            self.label = LabelWidget(
                text=f"Joining lobby at '{ip_address}'...",
                position=(engine.surface.get_width() // 2 - 220, engine.surface.get_height() // 2 - 40),
                font_size=50)

            # Navigation button
            self.menu.add.button("Back", (lambda: engine.load_view(AbstractView.make_view("join_game"))))
        else:
            self.labels = []
            self.players = engine.players

            if any([isinstance(player, RemotePlayer) for player in self.players]):
                engine.start_network()

            # Information labels
            for index, player in enumerate(self.players):
                label = LabelWidget(
                    text=f"Player {player.id + 1} : waiting",
                    position=(engine.surface.get_width() // 2 - 120, engine.surface.get_height() // 2 + index * 40 - 200),
                    font_size=50,
                    color="red")
                self.labels.append(label)

            self.menu.add.progress_bar("", progressbar_id="progressbar", default=0, width=200)

            # Navigation button
            self.menu.add.button("Back", (lambda: engine.load_view(AbstractView.make_view("players_configuration"))))


    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        if self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(engine.surface)

        if "ip_address" in self.parameters:
            self.label.draw(engine.surface)
        else:
            for label, player in zip(self.labels, self.players):
                if player.is_ready():
                    label.set_text(f"Player {player.id + 1} : ready")
                    label.set_color(pygame.Color("green"))
                label.draw(engine.surface)
            if all([player.is_ready() for player in self.players]):
                progressbar = self.menu.get_widget("progressbar")
                progressbar.set_value(progressbar.get_value() + 2)
                if progressbar.get_value() == 100:
                    engine.load_view(AbstractView.make_view("game", host=True))


AbstractView.VIEWS["waiting_room"] = WaitingRoomView
