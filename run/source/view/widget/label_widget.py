import pygame
import typing
from .abstract_widget import AbstractWidget


class LabelWidget(AbstractWidget):

    def __init__(
            self,
            text: 'str' = "",
            position: typing.Tuple['int', 'int'] = (0, 0),
            font_size: 'int' = 28,
            color: 'str' = "white",
            background_color: 'str' = "black"):
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color
        self.background_color = background_color
        self._build_rendered_text()

    def _build_rendered_text(self):
        font = pygame.font.Font(None, self.font_size)
        self.rendered_text = font.render(self.text, True, self.color, self.background_color)
        self.rect = pygame.Rect(self.position, self.rendered_text.get_size())

    def draw(self, surface: 'pygame.Surface'):
        surface.blit(self.rendered_text, self.position)

    def set_color(self, color: typing.Union[typing.Tuple['int', 'int', 'int'], 'str']):
        self.color = color
        self._build_rendered_text()

    def set_position(self, position: typing.Tuple['int', 'int']):
        self.position = position
        self._build_rendered_text()

    def set_text(self, text: 'str'):
        self.text = text
        self._build_rendered_text()

    def update(self, events: typing.List['pygame.event.Event']):
        pass
