import typing


class Cell:

    def __init__(self, x: 'int', y: 'int'):
        self.x = x
        self.y = y
        self.occupied_by: typing.Union['None', 'int'] = None

    def is_empty(self) -> 'bool':
        return self.occupied_by is None
