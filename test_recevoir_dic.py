import tkinter as tk

class QuoridorGUI:
    def __init__(self, num_players):
        self.num_players = num_players
        self.board_size = 9
        self.players = ['A', 'B', 'C', 'D'][:num_players]
        self.barriers_per_player = 10 // num_players
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pawns = {player: [(self.board_size // 2, (self.board_size // 2) - 1 + idx)] for idx, player in enumerate(self.players)}
        self.barriers = {player: self.barriers_per_player for player in self.players}
        self.current_player = self.players[0]

        self.root = tk.Tk()
        self.root.title("Quoridor")
        self.root.geometry("400x400")

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete(tk.ALL)
        square_size = 400 // self.board_size

        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = j * square_size
                y1 = i * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

                if (i, j) in self.pawns.values():
                    player = [player for player, pos in self.pawns.items() if pos == (i, j)][0]
                    self.canvas.create_oval(x1, y1, x2, y2, fill="blue" if player == 'A' else "red")

                if self.board[i][j] == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")

    def on_click(self, event):
        square_size = 400 // self.board_size
        row = event.y // square_size
        col = event.x // square_size

        if self.board[row][col] == ' ':
            if self.current_player == 'A':
                self.move_pawn(self.current_player, row, col)
            else:
                self.place_barrier(self.current_player, row, col)

            self.draw_board()

    def move_pawn(self, player, row, col):
        if (row, col) in self.pawns.values():
            return
        if row != self.pawns[player][0][0] and col != self.pawns[player][0][1]:
            return

        self.board[self.pawns[player][0][0]][self.pawns[player][0][1]] = ' '
        self.pawns[player] = [(row, col)]
        self.board[row][col] = player
        self.current_player = self.get_next_player(player)

    def place_barrier(self, player, row, col):
        if self.barriers[player] <= 0:
            return
        if row % 2 == 0 and col % 2 == 0:
            return
        if self.board[row][col] != ' ':
            return

        self.board[row][col] = '#'
        self.barriers[player] -= 1
        self.current_player = self.get_next_player(player)

    def get_next_player(self, player):
        idx = self.players.index(player)
        return self.players[(idx + 1) % self.num_players]


num_players = int(input("Enter the number of players (2 or 4): "))
game = QuoridorGUI(num_players)
