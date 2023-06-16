class QuoridorGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.board_size = 9
        self.players = ['A', 'B', 'C', 'D'][:num_players]
        self.barriers_per_player = 10 // num_players
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pawns = {player: [(self.board_size // 2, (self.board_size // 2) - 1 + idx)] for idx, player in enumerate(self.players)}
        self.barriers = {player: self.barriers_per_player for player in self.players}
        self.current_player = self.players[0]

    def print_board(self):
        print('+' + '-' * (self.board_size * 2 - 1) + '+')
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('+' + '-' * (self.board_size * 2 - 1) + '+')

    def move_pawn(self, player, direction):
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        current_pos = self.pawns[player][0]
        move = directions[direction]
        new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
        if self.is_valid_move(new_pos):
            self.board[current_pos[0]][current_pos[1]] = ' '
            self.board[new_pos[0]][new_pos[1]] = player
            self.pawns[player] = [new_pos]
            self.current_player = self.get_next_player(player)
            return True
        return False

    def place_barrier(self, player, row, col):
        if self.barriers[player] <= 0:
            return False
        if not self.is_valid_barrier_position(row, col):
            return False
        self.board[row][col] = '#'
        self.board[row][col + 1] = '#'
        self.board[row + 1][col] = '#'
        self.board[row + 1][col + 1] = '#'
        self.barriers[player] -= 1
        self.current_player = self.get_next_player(player)
        return True

    def is_valid_move(self, pos):
        if not (0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size):
            return False
        for pawn in self.pawns.values():
            if pos == pawn[0]:
                return False
        return True

    def is_valid_barrier_position(self, row, col):
        if not (0 <= row < self.board_size - 1 and 0 <= col < self.board_size - 1):
            return False
        if self.board[row][col] == '#' or self.board[row][col + 1] == '#' or self.board[row + 1][col] == '#' or self.board[row + 1][col + 1] == '#':
            return False
        return True

    def get_next_player(self, player):
        idx = self.players.index(player)
        return self.players[(idx + 1) % self.num_players]

    def play(self):
        while True:
            self.print_board()
            print(f"It's {self.current_player}'s turn.")
            action = input("Choose an action: [M]ove or [P]lace Barrier: ")
            if action.lower() == 'm':
                direction = input("Enter direction: [Up], [Down], [Left], [Right]: ").lower()
                if self.move_pawn(self.current_player, direction):
                    if self.check_win_condition():
                        print(f"Player {self.current_player} wins!")
                        break
            elif action.lower() == 'p':
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                if self.place_barrier(self.current_player, row, col):
                    if self.check_win_condition():
                        print(f"Player {self.current_player} wins!")
                        break
            else:
                print("Invalid action!")

    def check_win_condition(self):
        winning_rows = {'A': 0, 'B': self.board_size - 1}
        for player, pawns in self.pawns.items():
            for pawn in pawns:
                if pawn[0] == winning_rows[player]:
                    return True
        return False


num_players = int(input("Enter the number of players (2 or 4): "))
game = QuoridorGame(num_players)
game.play()
