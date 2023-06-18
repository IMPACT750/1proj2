import typing


class AbstractWidget:
    
    def draw(self, surface: 'pygame.Surface'):
        raise NotImplementedError()

    def update(self, events: typing.List['pygame.event.Event']):
        raise NotImplementedError()
