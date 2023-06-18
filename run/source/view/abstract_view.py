import typing


class AbstractView:

    VIEWS = {}

    @staticmethod
    def make_view(name: 'str', **parameters) -> 'AbstractView':
        return AbstractView.VIEWS[name](parameters)

    def __init__(self, parameters: typing.Dict['str', typing.Any]):
        self.parameters = parameters

    def initialize(self, engine: 'Engine'):
        raise NotImplementedError()

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        raise NotImplementedError()
