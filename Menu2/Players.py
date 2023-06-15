
class Player:

    def __init__(self, x, y,wall, ID):
        self.x = x
        self.y = y
        self.num_walls = wall
        self.ID = ID

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
