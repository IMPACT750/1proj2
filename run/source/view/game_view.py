import pygame
import typing
from ..configuration import Configuration
from .abstract_view import AbstractView
from .widget import ButtonWidget, LabelWidget


class GameView(AbstractView):

    def _draw_board(self, board: 'Board', surface: 'pygame.Surface', board_offset: typing.Tuple['int', 'int']):
        def draw_cell(x: 'int', y: 'int', color: 'str'):
            rect_value = (
                board_offset[0] + x * Configuration.CELL_SIZE,
                board_offset[1] + y * Configuration.CELL_SIZE,
                Configuration.CELL_SIZE,
                Configuration.CELL_SIZE)

            pygame.draw.rect(surface, color, rect_value)
        def draw_barrier(x: 'int', y: 'int', direction: 'str', color: 'str'):
            if direction == "horizontal":
                rect_value = (
                    board_offset[0] + x * Configuration.CELL_SIZE,
                    board_offset[1] + y * Configuration.CELL_SIZE + Configuration.CELL_SIZE - Configuration.BARRIER_SIZE,
                    Configuration.CELL_SIZE * 2,
                    Configuration.BARRIER_SIZE * 2)
            if direction == "vertical":
                rect_value = (
                    board_offset[0] + x * Configuration.CELL_SIZE + Configuration.CELL_SIZE - Configuration.BARRIER_SIZE,
                    board_offset[1] + y * Configuration.CELL_SIZE,
                    Configuration.BARRIER_SIZE * 2,
                    Configuration.CELL_SIZE * 2)

            pygame.draw.rect(surface, color, rect_value)

        # Draw cell
        for x in range(board.width):
            for y in range(board.height):
                draw_cell(x, y, "white" if (x + y) % 2 == 0 else "gray")

        # Draw barrier
        for x in range(board.width - 1):
            for y in range(board.height - 1):
                for direction in ("horizontal", "vertical"):
                    if board.barriers[(x, y, direction)].is_installed():
                        draw_barrier(x, y, direction, Configuration.PLAYER_COLORS[board.barriers[(x, y, direction)].installed_by])

        # Draw preview
        if board.preview_barrier is not None:
            x, y, direction, player_id = board.preview_barrier
            draw_barrier(x, y, direction, Configuration.PLAYER_LIGHT_COLORS[player_id])

    def _draw_informations(self, players: typing.List['Player'], player_turn: 'int', surface: 'pygame.Surface'):
        # Instruction label
        for player in players:
            if player.has_won():
                self.instruction_label.set_text(f"Player {player.id + 1} won !!!")
                self.instruction_label.set_color(Configuration.PLAYER_COLORS[player.id])
                break
        else:
            self.instruction_label.set_text(f"Player {player_turn + 1} turn")
            self.instruction_label.set_color(Configuration.PLAYER_COLORS[player_turn])
        self.instruction_label.draw(surface)

        # Score labels
        for index, player in enumerate(players):
            self.score_labels[index].set_text(f"Player {player.id + 1} : {player.score}")
            self.score_labels[index].draw(surface)

        # Navigation buttons
        if "host" in self.parameters:
            self.home_button.draw(surface)
            self.restart_button.draw(surface)

    def _draw_players(self, board: 'Board', players: typing.List['Player'], number_of_barriers: 'int', surface: 'pygame.Surface', board_offset: typing.Tuple['int', 'int']):
        def center_label(label: 'LabelWidget', position: typing.Tuple['int', 'int']):
            label.set_position((
                position[0] + Configuration.CELL_SIZE // 2 - label.rect.width // 2,
                position[1] + Configuration.CELL_SIZE // 2 - label.rect.height // 2))
        def draw_player(x: 'int', y: 'int', color: 'str') -> typing.Tuple['int', 'int']:
            position = (
                board_offset[0] + x * Configuration.CELL_SIZE,
                board_offset[1] + y * Configuration.CELL_SIZE)
            center = (position[0] + Configuration.CELL_SIZE // 2, position[1] + Configuration.CELL_SIZE // 2)
            radius = Configuration.CELL_SIZE // 2 - 5

            pygame.draw.circle(surface, color, center, radius)
            return position

        for index, player in enumerate(players):
            position = draw_player(player.x, player.y, Configuration.PLAYER_COLORS[index])
            self.player_barrier_labels[index].set_text(f"{player.number_of_barriers_placed}/{number_of_barriers}")
            center_label(self.player_barrier_labels[index], position)
            self.player_barrier_labels[index].draw(surface)

        # Draw preview
        if board.preview_player is not None:
            x, y, player_id = board.preview_player
            draw_player(x, y, Configuration.PLAYER_LIGHT_COLORS[player_id])

    def initialize(self, engine: 'Engine'):
        engine.initialize_game()

        # Player barrier labels
        self.player_barrier_labels = []

        for index, player in enumerate(engine.players):
            label = LabelWidget(
                f"{player.number_of_barriers_placed}/{engine.number_of_barriers}",
                font_size=30,
                color="black",
                background_color=Configuration.PLAYER_COLORS[index])
            self.player_barrier_labels.append(label)

        # Instruction label
        self.instruction_label = LabelWidget(
            f"Player {engine.player_turn + 1} turn",
            (20, 25),
            font_size=30,
            color=Configuration.PLAYER_COLORS[engine.player_turn])

        # Score labels
        self.score_labels = []

        for index, player in enumerate(engine.players):
            label = LabelWidget(
                f"Player {player.id + 1} : {player.score}",
                (engine.surface.get_width() - 140, 25 + index * 40),
                font_size=30,
                color=Configuration.PLAYER_COLORS[index])
            self.score_labels.append(label)

        # Navigation buttons
        if "host" in self.parameters:
            self.home_button = ButtonWidget(
                "Home",
                (engine.surface.get_width() - 140, engine.surface.get_height() - 65),
                font_size=50,
                onclick=(lambda: engine.load_view(AbstractView.make_view("home"))))
            self.restart_button = ButtonWidget(
                "Restart",
                (engine.surface.get_width() - 140, engine.surface.get_height() - 130),
                font_size=50,
                onclick=(lambda: engine.load_view(AbstractView.make_view("game", host=True))))

    def run(self, engine: 'Engine', events: typing.List['pygame.event.Event']):
        board_x_offset = (engine.surface.get_width() - (engine.board.width * Configuration.CELL_SIZE)) // 2
        board_y_offset = (engine.surface.get_height() - (engine.board.height * Configuration.CELL_SIZE)) // 2

        if "host" in self.parameters:
            self.home_button.update(events)
            self.restart_button.update(events)
        self._draw_informations(engine.players, engine.player_turn, engine.surface)
        self._draw_board(engine.board, engine.surface, (board_x_offset, board_y_offset))
        self._draw_players(engine.board, engine.players, engine.number_of_barriers, engine.surface, (board_x_offset, board_y_offset))


AbstractView.VIEWS["game"] = GameView
