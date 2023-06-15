import pygame
import sys
from Players import Player
from Boutons import Boutton
from Walls import Wall
import random

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Définition des couleurs
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Configuration de la surface d'affichage
DISPLAY_SIZE = (1000, 800)
surface = pygame.display.set_mode(DISPLAY_SIZE)

# Initialisation des variables globales
NUM_CELLS = 9
nb_player = 2
nb_barriere = 40 # valeur par défaut pour le nombre de barrières
font = pygame.font.Font(None, 36)

# Définition des constantes du jeu
CELL_SIZE = 50

# Calcul des dimensions du plateau en fonction de la taille des cellules
BOARD_WIDTH = NUM_CELLS * CELL_SIZE
BOARD_HEIGHT = NUM_CELLS * CELL_SIZE
BOARD_LEFT = (screen_width - BOARD_WIDTH) // 2
BOARD_TOP = (screen_height - BOARD_HEIGHT) // 2


def mouse_to_grid(x, y):
    grid_x = (x - BOARD_LEFT) // CELL_SIZE
    grid_y = (y - BOARD_TOP) // CELL_SIZE
    return grid_x, grid_y


def check_valid_player(nb_player):
    while nb_player != 2 and nb_player != 4:
        nb_player = int(input("nb de joueurs: "))
    return True

def create_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color):
    if check_valid_player(nb_player):
        for i in range(nb_player):
            pygame.draw.circle(screen, player_color[i], (
                BOARD_LEFT + player_in_game[i].x * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + player_in_game[i].y * CELL_SIZE + CELL_SIZE // 2),
                               CELL_SIZE // 2 - 5)
            board[player_in_game[i].x][player_in_game[i].y] = player_in_game[i].ID


walls = [[{"TOP": 0, "BOTTOM": 0, "LEFT": 0, "RIGHT": 0} for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]
board = [[0] * NUM_CELLS for _ in range(NUM_CELLS)]



def draw_board():
    for i in range(NUM_CELLS):

        for j in range(NUM_CELLS):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white,
                                 (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            else:
                pygame.draw.rect(screen, gray,
                                 (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_walls():
    for i in range(len(walls)):
        for j in range(len(walls[i])):
            if walls[i][j]["TOP"] == 1:
                pygame.draw.rect(screen, black, (
                    BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, 4))
            if walls[i][j]["BOTTOM"] == 1:
                pygame.draw.rect(screen, black, (
                    BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + (j + 1) * CELL_SIZE, CELL_SIZE, 4))
            if walls[i][j]["LEFT"] == 1:
                pygame.draw.rect(screen, black, (
                    BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, 4, CELL_SIZE))
            if walls[i][j]["RIGHT"] == 1:
                pygame.draw.rect(screen, black, (
                    BOARD_LEFT + (i + 1) * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, 4, CELL_SIZE))


pygame.display.flip()

game_turn=1
def player_turn(player, game_turn):
    game_turn=game_turn%(player+1)
    game_turn+=1
    if game_turn==player+1:
        return 1
    return game_turn

wall_orientation = None
wall_position = None
wall_button_clicked = False



# Créer une liste de boutons
buttons = [
    Boutton(550, 50, 100, 50, "Restart", gray),
    Boutton(350, 50, 150, 50, "Nouvelle Partie", gray),
    Boutton(10, 350, 100, 50, "HAUT", gray),
    Boutton(120, 350, 100, 50, "BAS", gray),
    Boutton(10, 450, 100, 50, "DROITE", gray),
    Boutton(120, 450, 100, 50, "GAUCHE", gray)
]
player1 = Player(NUM_CELLS // 2, 0,nb_barriere//nb_player, 1)
player2 = Player(NUM_CELLS // 2, NUM_CELLS - 1,nb_barriere//nb_player, 2)
player3 = Player(0, NUM_CELLS // 2,nb_barriere//nb_player, 3)
player4 = Player(NUM_CELLS - 1, NUM_CELLS // 2,nb_barriere//nb_player,4)
player_in_game = [player1, player2, player3, player4]

player_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner les boutons
    for button in buttons:
        button.draw(screen)

    # Mettre à jour l'affichage
    pygame.display.flip()


    # Boucle principale du jeu
    def place_wall_with_mouse(player, walls, mouse_x, mouse_y):
        if player.num_walls > 0:
            grid_x, grid_y = mouse_to_grid(mouse_x, mouse_y)
            aligned_mouse_x = grid_x * CELL_SIZE + BOARD_LEFT
            aligned_mouse_y = grid_y * CELL_SIZE + BOARD_TOP

            if abs(mouse_y - aligned_mouse_y) < abs(mouse_x - aligned_mouse_x):
                horizontal_wall = Wall(grid_x, grid_y, horizontal=True)
                if player.check_wall_collision(horizontal_wall, walls,NUM_CELLS):
                    walls.append(horizontal_wall)
                    player.num_walls -= 1
            else:
                vertical_wall = Wall(grid_x, grid_y, horizontal=False)
                if player.check_wall_collision(vertical_wall, walls,NUM_CELLS):
                    walls.append(vertical_wall)
                    player.num_walls -= 1




    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        if button.text == "HAUT":
                            wall_orientation = "HORIZONTAL"
                            wall_position = "TOP"
                            wall_button_clicked = True
                        elif button.text == "BAS":
                            wall_orientation = "HORIZONTAL"
                            wall_position = "BOTTOM"
                            wall_button_clicked = True
                        elif button.text == "DROITE":
                            wall_orientation = "VERTICAL"
                            wall_position = "RIGHT"
                            wall_button_clicked = True
                        elif button.text == "GAUCHE":
                            wall_orientation = "VERTICAL"
                            wall_position = "LEFT"
                            wall_button_clicked = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_to_grid(mouse_x, mouse_y)

                if event.button == 1:  # Left click to move player
                    for i in range(len(player_in_game)):
                        if game_turn == player_in_game[i].ID:
                            if i == 1:  # If it's player 2's turn
                                moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # List of possible moves
                                moved = False
                                while not moved:
                                    dx, dy = random.choice(moves)  # Choose a random move
                                    new_x = player_in_game[i].x + dx
                                    new_y = player_in_game[i].y + dy
                                    moved = player_in_game[i].move(new_x, new_y, walls, NUM_CELLS, board)
                                game_turn = player_turn(nb_player, game_turn)
                            else:
                                if (abs(grid_x - player_in_game[i].x) <= 1 and grid_y == player_in_game[i].y) or (
                                        abs(grid_y - player_in_game[i].y) <= 1 and grid_x == player_in_game[i].x):
                                    if player_in_game[i].move(grid_x, grid_y, walls, NUM_CELLS, board):
                                        game_turn = player_turn(nb_player,game_turn)

                elif event.button == 3:  # Right click to place a wall
                    for i in range(len(player_in_game)):
                        if game_turn == player_in_game[i].ID:
                            if i == 1:  # If it's player 2's turn and they still have walls
                                # Code for player 2 placing walls randomly
                                possible_positions = [(x, y) for x in range(NUM_CELLS) for y in range(NUM_CELLS)]
                                random.shuffle(possible_positions)
                                for grid_x, grid_y in possible_positions:
                                    wall_orientation = random.choice(["HORIZONTAL", "VERTICAL"])
                                    wall_position = random.choice(["TOP", "BOTTOM"]) if wall_orientation == "HORIZONTAL" else random.choice(["LEFT", "RIGHT"])
                                    if wall_orientation == "HORIZONTAL":
                                        if walls[grid_x][grid_y][wall_position] == 0:  # Check if a wall can be placed at this location
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "TOP":
                                                walls[grid_x][grid_y - 1]["BOTTOM"] = 1
                                            else:
                                                walls[grid_x][grid_y + 1]["TOP"] = 1
                                            player_in_game[i].num_walls -= 1
                                            game_turn = player_turn(nb_player, game_turn)
                                            break
                                    elif wall_orientation == "VERTICAL":
                                        if walls[grid_x][grid_y][wall_position] == 0:  # Check if a wall can be placed at this location
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "LEFT":
                                                walls[grid_x - 1][grid_y]["RIGHT"] = 1
                                            else:
                                                walls[grid_x + 1][grid_y]["LEFT"] = 1
                                            player_in_game[i].num_walls -= 1
                                            game_turn = player_turn(nb_player, game_turn)
                                            break
                            elif i == 0:  # If it's player 1's turn
                                if wall_button_clicked:  # Only if a wall button has been clicked
                                    grid_x, grid_y = mouse_to_grid(mouse_x, mouse_y)
                                    if wall_orientation == "HORIZONTAL":
                                        if walls[grid_x][grid_y][wall_position] == 0:  # Check if a wall can be placed at this location
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "TOP":
                                                walls[grid_x][grid_y - 1]["BOTTOM"] = 1
                                            else:
                                                walls[grid_x][grid_y + 1]["TOP"] = 1
                                            player_in_game[i].num_walls -= 1
                                            game_turn = player_turn(nb_player, game_turn)
                                    elif wall_orientation == "VERTICAL":
                                        if walls[grid_x][grid_y][wall_position] == 0:  # Check if a wall can be placed at this location
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "LEFT":
                                                walls[grid_x - 1][grid_y]["RIGHT"] = 1
                                            else:
                                                walls[grid_x + 1][grid_y]["LEFT"] = 1
                                            player_in_game[i].num_walls -= 1
                                            game_turn = player_turn(nb_player, game_turn)
                                    wall_button_clicked = False




        # Dessin du plateau de jeu, des joueurs et des murs
        draw_board()
        create_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color)
        draw_walls()
        num_barrieres_text = font.render("Barrières restantes : " + str(nb_barriere), True, white)
        screen.blit(num_barrieres_text, (10, 10))

        # Actualisation de la fenêtre
        pygame.display.flip()
        # Limitez la vitesse de rafraîchissement de l'écran à 60 images par seconde
        pygame.time.Clock().tick(60)

    pygame.quit()