import pygame
import typing
from .label_widget import LabelWidget


class ButtonWidget(LabelWidget):

    def __init__(
            self,
            text: 'str' = "",
            position: typing.Tuple['int', 'int'] = (0, 0),
            font_size: 'int' = 28,
            color: 'str' = "black",
            background_color: 'str' = "gray",
            onclick: typing.Callable = None):
        super().__init__(text, position, font_size, color, background_color)
        self.onclick = onclick

    def draw(self, surface: 'pygame.Surface'):
        pygame.draw.rect(surface, self.background_color, self.rect)
        super().draw(surface)

    def update(self, events: typing.List['pygame.event.Event']):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self.onclick:
                        self.onclick()
