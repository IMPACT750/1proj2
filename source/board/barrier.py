import typing


class Barrier:

    def __init__(self, x: 'int', y: 'int', direction: 'str'):
        self.x = x
        self.y = y
        self.direction = direction
        self.installed_by: typing.Union['None', 'int'] = None

    def is_installed(self) -> 'bool':
        return self.installed_by is not None
