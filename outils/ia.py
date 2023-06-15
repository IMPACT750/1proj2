import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Définition des couleurs
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Définition des constantes du jeu
CELL_SIZE = 50
NUM_CELLS = 9
BOARD_WIDTH = NUM_CELLS * CELL_SIZE
BOARD_HEIGHT = NUM_CELLS * CELL_SIZE
BOARD_LEFT = (screen_width - BOARD_WIDTH) // 2
BOARD_TOP = (screen_height - BOARD_HEIGHT) // 2

# Définition de la classe Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_walls = 10

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

# Initialisation des joueurs
player1 = Player(4, 0)
player2 = Player(4, 8)

# Dessin des cases vides sur le plateau de jeu
def draw_board():
    for i in range(NUM_CELLS):
        for j in range(NUM_CELLS):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white, (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, gray, (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Dessin des joueurs
def draw_players():
    pygame.draw.circle(screen, (255, 0, 0), (BOARD_LEFT + player1.x * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP + player1.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
    pygame.draw.circle(screen, (0, 0, 255), (BOARD_LEFT + player2.x * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP + player2.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

# Actualisation de la fenêtre
pygame.display.flip()

# Initialisation du tour de jeu
current_player = 1

# Boucle principale du jeu
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            # Mouvements du joueur 1
            if current_player == 1:
                if event.key == pygame.K_UP:
                    player1.move_up()
                elif event.key == pygame.K_DOWN:
                    player1.move_down()
                elif event.key == pygame.K_LEFT:
                    player1.move_left()
                elif event.key == pygame.K_RIGHT:
                    player1.move_right()

                # Changement de tour de jeu
                current_player = 2

    # Mouvements du joueur automatique
    if current_player == 2:
        player2_move = random.choice(['up', 'down', 'left', 'right'])
        if player2_move == 'up':
            player2.move_up()
        elif player2_move == 'down':
            player2.move_down()
        elif player2_move == 'left':
            player2.move_left()
        elif player2_move == 'right':
            player2.move_right()

        # Changement de tour de jeu
        current_player = 1

    # Redessin du plateau de jeu
    screen.fill(black)
    draw_board()
    draw_players()
    pygame.display.flip()


# Définition de la classe Wall
class Wall:
    def __init__(self, x, y, horizontal=True):
        self.x = x
        self.y = y
        self.horizontal = horizontal

    def draw(self):
        if self.horizontal:
            pygame.draw.rect(screen, black, (BOARD_LEFT + self.x * CELL_SIZE, BOARD_TOP + self.y * CELL_SIZE + CELL_SIZE // 2 - 2, CELL_SIZE, 4))
        else:
            pygame.draw.rect(screen, black, (BOARD_LEFT + self.x * CELL_SIZE + CELL_SIZE // 2 - 2, BOARD_TOP + self.y * CELL_SIZE, 4, CELL_SIZE))

# Initialisation des murs
walls = []
for i in range(NUM_CELLS - 1):
    for j in range(NUM_CELLS - 1):
        walls.append(Wall(i, j))
# Dessin des murs
for wall in walls:
    wall.draw()


class Player:
    # ...

    def place_horizontal_wall(self, x, y):
        if self.num_walls > 0:
            wall = Wall(x, y)
            walls.append(wall)
            self.num_walls -= 1
            return True
        else:
            return False


class Wall:
    # ...

    def move_up(self):
        if self.y > 0:
            self.y -= 1

    def move_down(self):
        if self.y < NUM_CELLS - 2:
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < NUM_CELLS - 2:
            self.x += 1
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        elif event.key == pygame.K_UP:
            player.move_up()
        elif event.key == pygame.K_DOWN:
            player.move_down()
        elif event.key == pygame.K_LEFT:
            player.move_left()
        elif event.key == pygame.K_RIGHT:
            player.move_right()
        elif event.key == pygame.K_h:
            player.place_horizontal_wall(player.current_cell_x, player.current_cell_y)
        elif event.key == pygame.K_w:
            for wall in walls:
                if not wall.horizontal and wall.x == player.current_cell_x and wall.y == player.current_cell_y - 1:
                    wall.move_up()
                    break
        elif event.key == pygame.K_a:
            for wall in walls:
                if wall.horizontal and wall.x == player.current_cell_x - 1 and wall.y == player.current_cell_y:
                    wall.move_left()
                    break
        elif event.key == pygame.K_s:
            for wall in walls:
                if not wall.horizontal and wall.x == player.current_cell_x and wall.y == player.current_cell_y:
                    wall.move_down()
                    break
        elif event.key == pygame.K_d:
            for wall in walls:
                if wall.horizontal and wall.x == player.current_cell_x and wall.y == player.current_cell_y:
                    wall.move_right()
                    break
