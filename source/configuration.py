import typing


class Configuration:
    BACKGROUND_COLOR: typing.Tuple['int', 'int', 'int']             = (0, 0, 0)
    BARRIER_SIZE: 'int'                                             = 3
    BOARD_DIMENSIONS: typing.Tuple[typing.Tuple['int', 'int'], ...] = ((5, 5), (7, 7), (9, 9), (11, 11))
    CELL_SIZE: 'int'                                                = 60
    FRAME_PER_SECOND: 'int'                                         = 60
    NUMBER_OF_BARRIERS: typing.Tuple['int', ...]                    = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    NUMBER_OF_PLAYERS: typing.Tuple['int', 'int']                   = (2, 4)
    PLAYER_TYPES: typing.Tuple['str', 'str', 'str']                 = ("Local Player", "Remote Player", "AI")
    PLAYER_COLORS: typing.Tuple['str', 'str', 'str', 'str']         = ("red", "blue", "green", "yellow")
    PLAYER_LIGHT_COLORS: typing.Tuple['str', 'str', 'str', 'str']   = ("lightcoral", "steelblue3", "lightgreen", "lightgoldenrod1")
    SERVER_IP: 'str'                                                = "localhost"
    SERVER_PORT: 'int'                                              = 12800
    TITLE: 'str'                                                    = "Quoridor Game"
    WINDOW_SIZE: typing.Tuple['int', 'int']                         = (1000, 800)
