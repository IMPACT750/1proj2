import typing


def path_finder(start_cell: typing.Tuple['int', 'int'], targets: typing.List['int'], board: 'Board') -> True:
    queue = [(start_cell, _heuristic(start_cell, targets, board))]
    visited = []

    while queue:
        cell = _extract_min_cell(queue)
    
        visited.append(cell)
        if cell in targets:
           return True

        for neighbor in board.get_possibles_moves(*cell):
            if neighbor not in visited:
                queue.append((neighbor, _heuristic(neighbor, targets, board)))

    return False

def _extract_min_cell(queue: typing.List[typing.Tuple[typing.Tuple['int', 'int'], 'int']]) -> typing.Tuple['int', 'int']:
    min_index, min_value = 0, queue[0][1]

    for index, (_, value) in enumerate(queue):
        if value < min_value:
            min_index, min_value = min_index, value
    return queue.pop(min_index)[0]

def _heuristic(cell: typing.Tuple['int', 'int'], targets: typing.List[typing.Tuple['int', 'int']], board: 'Board') -> 'int':
    def _manhattan_distance(cell: typing.Tuple['int', 'int'], target: typing.Tuple['int', 'int']) -> 'int':
        return abs(cell[0] - target[0]) + abs(cell[1] - target[1])

    return min([_manhattan_distance(cell, target) for target in targets])
