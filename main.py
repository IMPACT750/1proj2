import pygame
import sys
from Players import Player
from Boutons import Boutton
from Walls import Wall
from fonction_reseau import *



pygame.init()
font = pygame.font.Font(None, 32)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
player_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]


def mouse_to_grid(x, y,CELL_SIZE,BOARD_LEFT,BOARD_TOP):
    grid_x = (x - BOARD_LEFT) // CELL_SIZE
    grid_y = (y - BOARD_TOP) // CELL_SIZE
    return grid_x, grid_y


def draw_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color,screen,board):
    for i in range(nb_player):
        pygame.draw.circle(screen, player_color[i], (
            BOARD_LEFT + player_in_game[i].x * CELL_SIZE + CELL_SIZE // 2,
            BOARD_TOP + player_in_game[i].y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2 - 5)
        board[player_in_game[i].x][player_in_game[i].y] = player_in_game[i].ID


def draw_board(NUM_CELLS,screen,BOARD_LEFT,CELL_SIZE,BOARD_TOP):
    for i in range(NUM_CELLS):

        for j in range(NUM_CELLS):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white,
                                 (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            else:
                pygame.draw.rect(screen, gray,
                                 (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_walls(walls,screen,BOARD_LEFT,CELL_SIZE,BOARD_TOP):
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


def place_wall_with_mouse(player, walls, mouse_x, mouse_y, CELL_SIZE,BOARD_LEFT,BOARD_TOP,NUM_CELLS):
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


def condition_victoire(tableau, players):
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[j][0] == 2:
                print("joueur 2 a gagné")
                players[1].win()  # Augmenter le score du joueur 2
                return 2
            elif tableau[j][len(tableau[i])-1] == 1:
                print("joueur 1 a gagné")
                players[0].win()  # Augmenter le score du joueur 1
                return 1
            elif j == 0 and tableau[0][i] == 4:
                print("joueur 3 a gagné")
                players[2].win()  # Augmenter le score du joueur 3
                return 3
            elif tableau[len(tableau)-1][i] == 3:
                print("joueur 4 a gagné")
                players[3].win()  # Augmenter le score du joueur 4
                return 4
    return 0


def reset_game(NUM_CELLS, barriere_max, nb_player, player_color, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP,player_in_game,connection):
    global game_turn, wall_button_clicked, wall_orientation, walls, board, nb_barriere
    # Réinitialiser les variables globales
    game_turn = 1
    wall_button_clicked = False
    wall_orientation = None
    nb_barriere =barriere_max # Le nombre initial de barrières par joueur
    point=[]
    for i in player_in_game:
        point.append(i.score)
    # Créer une nouvelle grille de jeu (tableau 2D)
    board = [[0 for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]
    walls=[[{"TOP": 0, "BOTTOM": 0, "LEFT": 0, "RIGHT": 0} for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]
    player_in_game = Player.create_players(Player, nb_player, nb_barriere, NUM_CELLS)
    for i in range(len(player_in_game)):
        player_in_game[i].score=point[i]
    jeux(walls, screen, CELL_SIZE, BOARD_LEFT, BOARD_TOP, NUM_CELLS, player_in_game, player_color, board, nb_player,nb_barriere, barriere_max,connection)

def draw_score_and_barriers(screen, player_in_game, game_turn, font, player_color):
    # Zone en haut à gauche pour le nombre de barrières
    for i, player in enumerate(player_in_game):
        pygame.draw.rect(screen, (0, 0, 0), (10, 10 + i * 30, 200, 30))  # Effacer la zone de texte précédente
        num_barrieres_text = font.render("Barrières Joueur " + str(player.color) + " : " + str(player.num_walls), True, player_color[i])
        screen.blit(num_barrieres_text, (10, 10 + i * 30))

    # Zone en haut à droite pour le tour du joueur
    pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() - 210, 10, 200, 30))  # Effacer la zone de texte précédente
    game_turn_text = font.render("Tour du Joueur : " + str(player_in_game[game_turn-1].color), True, player_color[game_turn-1])
    screen.blit(game_turn_text, (screen.get_width() - game_turn_text.get_width() - 10, 10))

    # Utilisation d'un décalage pour l'alignement des scores des joueurs
    offset_x = [screen.get_width() // 2 - 150, screen.get_width() // 2 + 150]  # Décalage en x pour les scores
    offset_y = screen.get_height() - 80  # Décalage initial en y

    for i, player in enumerate(player_in_game):
        pygame.draw.rect(screen, (0, 0, 0), (offset_x[i % 2] - 100, offset_y - ((1 - i // 2) * 40), 200, 30))  # Effacer la zone de texte précédente
        score_text = font.render("Score du joueur " + str(player.color) + " : " + str(player.score), True,  player_color[i])
        screen.blit(score_text, (offset_x[i % 2] - score_text.get_width() // 2, offset_y - ((1 - i // 2) * 40)))


def jeux(walls, screen, CELL_SIZE, BOARD_LEFT, BOARD_TOP, NUM_CELLS, player_in_game, player_color, board, nb_player,barriere_max,connection):
    global game_turn, wall_button_clicked, wall_orientation

    running = True
    game_over = False
    is_your_turn = True

    while running:
        if connection != 0 and is_your_turn is False: 
            new_tableau = recevoir_tableau_jeu(connection)  # Recevoir le tableau de jeu mis à jour du serveur
            if new_tableau:
                board = new_tableau["board"]
                walls = new_tableau["walls"]
                player_in_game = new_tableau["player_in_game"]
                is_your_turn = True


        else:
            screen.fill((0, 0, 0))
            draw_board(NUM_CELLS, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP)
            draw_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color, screen, board)
            draw_score_and_barriers(screen, player_in_game, game_turn, font, player_color)
            
            for button in buttons:
                button.draw(screen)
            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


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

                        if button.rect.collidepoint(mouse_x, mouse_y):
                            if button.text == "Restart" or button.text == "Nouvelle Partie":
                                reset_game(NUM_CELLS, barriere_max, nb_player, player_color, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP,player_in_game,connection)
                if game_over:  # Si le jeu est terminé, ignorer tous les événements
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_to_grid(mouse_x, mouse_y, CELL_SIZE, BOARD_LEFT, BOARD_TOP)

                    if event.button == 1:  # Clic gauche pour déplacer le joueur
                        for i in range(len(player_in_game)):
                            if game_turn == player_in_game[i].ID:
                                if (abs(grid_x - player_in_game[i].x) <= 1 and grid_y == player_in_game[i].y) or (
                                        abs(grid_y - player_in_game[i].y) <= 1 and grid_x == player_in_game[i].x):
                                    if player_in_game[i].move(grid_x, grid_y, walls, NUM_CELLS, board):
                                        if connection != 0:
                                            envoyer_tableau_jeu(connection, board, walls,player_in_game)
                                        game_turn = player_turn(nb_player, game_turn)
                                        winner = condition_victoire(board, player_in_game)
                                        if winner != 0:
                                            game_over = True  # Mettre fin au jeu
                                            print("Le jeu est terminé. Le joueur", winner, "a gagné!")
                                            break
                                        is_your_turn = False
                                    break

                    elif event.button == 3:  # Clic droit pour placer un mur
                        if wall_button_clicked:
                            for i in range(len(player_in_game)):
                                if game_turn == player_in_game[i].ID:
                                    if player_in_game[i].num_walls > 0:
                                        if wall_orientation == "HORIZONTAL":
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "TOP":
                                                walls[grid_x][grid_y - 1]["BOTTOM"] = 1
                                                walls[grid_x + 1][grid_y - 1]["BOTTOM"] = 1
                                            else:
                                                walls[grid_x][grid_y + 1]["TOP"] = 1
                                                walls[grid_x + 1][grid_y + 1]["TOP"] = 1
                                        else:
                                            walls[grid_x][grid_y][wall_position] = 1
                                            if wall_position == "LEFT":
                                                walls[grid_x - 1][grid_y]["RIGHT"] = 1
                                                walls[grid_x - 1][grid_y + 1]["RIGHT"] = 1
                                            else:
                                                walls[grid_x + 1][grid_y]["LEFT"] = 1
                                                walls[grid_x + 1][grid_y + 1]["LEFT"] = 1
                                        player_in_game[i].num_walls -= 1
                                        game_turn = player_turn(nb_player, game_turn)
                                        if connection != 0:
                                            envoyer_tableau_jeu(connection, board, walls, player_in_game)
                                        break
                            wall_button_clicked = False


            # Dessin du plateau de jeu, des joueurs et des murs
        draw_board(NUM_CELLS, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP)
        draw_walls(walls, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP)
        draw_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color, screen, board)
        draw_score_and_barriers(screen, player_in_game, game_turn, font, player_color)
        # Mettre à jour l'affichage
        pygame.display.flip()
        pygame.time.wait(50)  # Ajoutez cette ligne pour contrôler la vitesse de rafraîchissement de l'écran
