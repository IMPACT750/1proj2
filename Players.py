
class Player:

    def __init__(self, x, y,wall, ID,score,color,arrive_x,arrive_y):
        self.x = x
        self.y = y
        self.num_walls = wall
        self.ID = ID
        self.score = score
        self.color = color
        self.arrive_x = arrive_x
        self.arrive_y = arrive_y
    def move(self, x, y,walls,NUM_CELLS,board):
        direction = ""
        if (abs(x - self.x) <= 1 and y == self.y) or (abs(y - self.y) <= 1 and x == self.x):
            if 0 <= x < NUM_CELLS and 0 <= y < NUM_CELLS:
                if x > self.x:
                    direction = "RIGHT"
                elif x < self.x:
                    direction = "LEFT"
                elif y > self.y:
                    direction = "BOTTOM"
                elif y < self.y:
                    direction = "TOP"
                if board[x][y] != 0:
                    if x > self.x:
                        x += 1
                        direction = "RIGHT"
                    elif x < self.x:
                        x -= 1
                        direction = "LEFT"
                    elif y > self.y:
                        y += 1
                        direction = "BOTTOM"
                    elif y < self.y:
                        y -= 1
                        direction = "TOP"
                if self.check_collision(x, y, board):
                    if self.check_wall_collision(x, y, direction, walls,NUM_CELLS):
                        board[self.x][self.y] = 0
                        self.x = x
                        self.y = y
                        board[self.x][self.y] = self.ID
                        return True
                else:
                    return False

    def check_collision(self, x, y, tableau):
        if 0 <= x < len(tableau) and 0 <= y < len(tableau[x]):
            if tableau[x][y] == 0:
                return True
        return False

    def check_wall_collision(self, x, y, direction, walls,NUM_CELLS):
        if 0 <= x < NUM_CELLS and 0 <= y < NUM_CELLS:
            if direction != "" and walls[self.x][self.y][direction] == 0:
                return True
        return False

    def create_players(self, num_players, wall, NUM_CELLS):
        players = []
        centers = [(NUM_CELLS // 2, 0), (NUM_CELLS // 2, NUM_CELLS - 1), (0, NUM_CELLS // 2),
                   (NUM_CELLS - 1, NUM_CELLS // 2)]
        arrive_coords = [(NUM_CELLS // 2, NUM_CELLS - 1), (NUM_CELLS // 2, 0), (NUM_CELLS - 1, NUM_CELLS // 2),
                         (0, NUM_CELLS // 2)]
        colors = ["rouge", "bleu", "vert", "jaune"]  # List of colors
        if num_players == 2:
            for i in range(2):
                players.append(Player(centers[i][0], centers[i][1], wall // 4, i + 1, 0, colors[i],
                                      arrive_coords[i][0], arrive_coords[i][1]))

        elif num_players == 4:
            for i in range(4):
                players.append(Player(centers[i][0], centers[i][1], wall // 4, i + 1, 0, colors[i],
                                      arrive_coords[i][0], arrive_coords[i][1]))
        else:
            raise ValueError("Invalid number of players. Only 2 or 4 are accepted.")
        return players

    def win(self):
        self.score+=1
