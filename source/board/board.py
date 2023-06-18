import typing
from ..algorithm import path_finder
from .cell import Cell
from .barrier import Barrier


class Board:

    def __init__(self):
        self.barriers = {}
        self.cells = {}
        self.width: 'int' = None
        self.height: 'int' = None
        self.preview_barrier: typing.Tuple['int', 'int', 'str', 'int'] = None
        self.preview_player: typing.Tuple['int', 'int', 'int'] = None

    def get_possibles_moves(self, x: 'int', y: 'int') -> typing.List[typing.Tuple['int', 'int']]:
        possibles_moves = []

        for move in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not (0 <= move[0] < self.width and 0 <= move[1] < self.height):
                continue
            if not self.cells[move].is_empty():
                for jump_move in [(move[0] + 1, move[1]), (move[0] - 1, move[1]), (move[0], move[1] + 1), (move[0], move[1] - 1)]:
                    if jump_move != (x, y) and self.is_possible_move(x, y, *jump_move):
                        possibles_moves.append(jump_move)
            else:
                if self.is_possible_move(x, y, *move):
                    possibles_moves.append(move)
        return possibles_moves

    def initialize(self, dimensions: typing.Tuple['int', 'int']):
        self.width, self.height = dimensions

        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = Cell(x, y)
                for direction in ("horizontal", "vertical"):
                    if x == self.width - 1 or y == self.height - 1:
                        continue
                    self.barriers[(x, y, direction)] = Barrier(x, y, direction)

    def is_possible_installation(self, x: 'int', y: 'int', direction: 'str', number_of_barriers_left: 'int', players: typing.List['AbstractPlayer']) -> 'bool':
        # Check if is inside the board
        if not (0 <= x < self.width - 1 and 0 <= y < self.height - 1):
            return False

        # Check if player has barriers left
        if number_of_barriers_left <= 0:
            return False

        # Check if is already installed (direction)
        for offset in ("horizontal", "vertical"):
            if self.barriers[(x, y, offset)].is_installed():
                return False

        # Check if is already installed (around)
        if direction == "horizontal":
            offsets = [(-1, 0), (1, 0)]
        elif direction == "vertical":
            offsets = [(0, -1), (0, 1)]
        else:
            return False

        for offset in offsets:
            if not (0 <= x + offset[0] < self.width - 1 and 0 <= y + offset[1] < self.height - 1):
                continue
            if self.barriers[(x + offset[0], y + offset[1], direction)].is_installed():
                return False

        # Check if a player is not blocked
        self.barriers[(x, y, direction)].installed_by = -1 # Temporary installation by nobody
        for player in players:
            if path_finder((player.x, player.y), player.targets, self) is False:
                self.barriers[(x, y, direction)].installed_by = None
                return False
        self.barriers[(x, y, direction)].installed_by = None

        return True

    def is_possible_move(self, start_x: 'int', start_y: 'int', end_x: 'int', end_y: 'int') -> 'bool':
        def _barrier_block_move(x: 'int', y: 'int', direction: typing.Tuple['int', 'int']) -> 'bool':
            barrier_positions = {
                ( 0, -1): [(x - 1, y - 1, "horizontal"), (x,     y - 1, "horizontal")],
                ( 1,  0): [(x,     y - 1, "vertical"),   (x,     y,     "vertical")  ],
                ( 0,  1): [(x,     y,     "horizontal"), (x - 1, y,     "horizontal")],
                (-1,  0): [(x - 1, y,     "vertical"),   (x - 1, y - 1, "vertical")  ],
            }[direction]

            for barrier_position in barrier_positions:
                if not (0 <= barrier_position[0] < self.width - 1 and 0 <= barrier_position[1] < self.height - 1):
                    continue
                if self.barriers[barrier_position].is_installed():
                    return True
            return False
        def _reduce_direction(direction: typing.Tuple['int', 'int']) -> typing.Tuple['int', 'int']:
            return (min(1, max(-1, direction[0])), min(1, max(-1, direction[1])))

        # Check if is inside the board
        if not (0 <= end_x < self.width and 0 <= end_y < self.height):
            return False

        # Check if cell is occupied
        if not self.cells[(end_x, end_y)].is_empty():
            return False

        direction = (end_x - start_x, end_y - start_y)

        # Check if can basic move
        if direction in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if _barrier_block_move(start_x, start_y, direction) is True:
                return False
            return True

        # Check if can jump over a player
        if direction in ((0, -2), (2, 0), (0, 2), (-2, 0)):
            direction = _reduce_direction(direction)

            if _barrier_block_move(start_x, start_y, direction) is True:
                return False            
            if self.cells[(start_x + direction[0], start_y + direction[1])].is_empty():
                return False
            if _barrier_block_move(start_x + direction[0], start_y + direction[1], direction) is True:
                return False
            return True

        # Check if can take diagonal
        if direction in ((1, -1), (1, 1), (-1, 1), (-1, -1)):
            if not self.cells[(start_x + direction[0], start_y)].is_empty():
                if 0 <= start_x + direction[0] * 2 < self.width:
                    if _barrier_block_move(start_x + direction[0], start_y, (direction[0], 0)) is False \
                    and self.cells[(start_x + direction[0] * 2, start_y)].is_empty():
                        return False
                if _barrier_block_move(start_x, start_y, (direction[0], 0)) is True:
                    return False
                if _barrier_block_move(start_x + direction[0], start_y, (0, direction[1])) is True:
                    return False
                return True
            elif not self.cells[(start_x, start_y + direction[1])].is_empty():
                if 0 <= start_y + direction[1] * 2 < self.height:
                    if _barrier_block_move(start_x, start_y + direction[1], (0, direction[1])) is False \
                    and self.cells[(start_x, start_y + direction[1] * 2)].is_empty():
                        return False
                if _barrier_block_move(start_x, start_y, (0, direction[1])) is True:
                    return False
                if _barrier_block_move(start_x, start_y + direction[1], (direction[0], 0)) is True:
                    return False
                return True
            else:
                return False

        return False
