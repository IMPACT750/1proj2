import pygame
import typing
from ..configuration import Configuration
from .abstract_player import AbstractPlayer


class LocalPlayer(AbstractPlayer):



    def _mouse_to_barrier_position(self, x: 'int', y: 'int', board_offset: typing.Tuple['int', 'int']) -> typing.Tuple['int', 'int', 'str']:
        board_x_offset, board_y_offset = board_offset

        barrier_x = (x - (board_x_offset + Configuration.CELL_SIZE // 2)) // Configuration.CELL_SIZE
        barrier_y = (y - (board_y_offset + Configuration.CELL_SIZE // 2)) // Configuration.CELL_SIZE

        relative_x = x - (board_x_offset + Configuration.CELL_SIZE // 2) - barrier_x * Configuration.CELL_SIZE
        relative_y = y - (board_y_offset + Configuration.CELL_SIZE // 2) - barrier_y * Configuration.CELL_SIZE

        if Configuration.CELL_SIZE // 3 <= relative_x <= Configuration.CELL_SIZE * 2 // 3:
            return barrier_x, barrier_y, "vertical"
        elif Configuration.CELL_SIZE // 3 <= relative_y <= Configuration.CELL_SIZE * 2 // 3:
            return barrier_x, barrier_y, "horizontal"
        else:
            return -1, -1, ""

    def _mouse_to_cell_position(self, x: 'int', y: 'int', board_offset: typing.Tuple['int', 'int']) -> typing.Tuple['int', 'int']:
        board_x_offset, board_y_offset = board_offset

        return (x - board_x_offset) // Configuration.CELL_SIZE, (y - board_y_offset) // Configuration.CELL_SIZE

    def _preview_install(self, x: 'int', y: 'int', direction: 'str', board: 'Board'):
        board.preview_barrier = (x, y, direction, self.id)

    def _preview_move(self, x: 'int', y: 'int', board: 'Board'):
        board.preview_player = (x, y, self.id)

    def _unpreview_install(self, board: 'Board'):
        board.preview_barrier = None

    def _unpreview_move(self, board: 'Board'):
        board.preview_player = None

    def action(self, engine: 'Engine', events: typing.List['pygame.event.Event']) -> 'bool':
        board_x_offset = (engine.surface.get_width() - (engine.board.width * Configuration.CELL_SIZE)) // 2
        board_y_offset = (engine.surface.get_height() - (engine.board.height * Configuration.CELL_SIZE)) // 2

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x, y = self._mouse_to_cell_position(*pygame.mouse.get_pos(), (board_x_offset, board_y_offset))

                if engine.board.is_possible_move(self.x, self.y, x, y) is True:
                    self.move(x, y, engine.board)
                    self._unpreview_install(engine.board)
                    self._unpreview_move(engine.board)
                    engine.update_to_network()
                    self.jouer_son_pion("source/pawn.wav")
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                x, y, direction = self._mouse_to_barrier_position(*pygame.mouse.get_pos(), (board_x_offset, board_y_offset))

                if engine.board.is_possible_installation(x, y, direction, engine.number_of_barriers - self.number_of_barriers_placed, engine.players) is True:
                    self.install(x, y, direction, engine.board)
                    self._unpreview_install(engine.board)
                    self._unpreview_move(engine.board)
                    engine.update_to_network()
                    self.jouer_son_barriere("source/barriere.wav")
                    return True
            else:
                barrier_position = self._mouse_to_barrier_position(*pygame.mouse.get_pos(), (board_x_offset, board_y_offset))
                cell_position = self._mouse_to_cell_position(*pygame.mouse.get_pos(), (board_x_offset, board_y_offset))

                if engine.board.is_possible_installation(*barrier_position, engine.number_of_barriers - self.number_of_barriers_placed, []) is True:
                    self._preview_install(*barrier_position, engine.board)

                else:
                    self._unpreview_install(engine.board)
                if engine.board.is_possible_move(self.x, self.y, *cell_position) is True:
                    self._preview_move(*cell_position, engine.board)
                else:
                    self._unpreview_move(engine.board)

        return False

    def is_ready(self) -> 'bool':
        return True

    def jouer_son_pion(self, fichier_son):
        son = pygame.mixer.Sound(fichier_son)
        son.play()
    def jouer_son_barriere(self, fichier_son):
        son = pygame.mixer.Sound(fichier_son)
        son.play()



AbstractPlayer.PLAYERS[Configuration.PLAYER_TYPES[0]] = LocalPlayer
