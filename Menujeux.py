import pygame
import pygame_menu
import subprocess
from main import *
from Players import Player
from fonction_reseau import *
from Menu2 import *

# Variable globale
CELL_SIZE = 50
NUM_CELLS = 9
nb_player = 2
nb_barriere = 20


# Fonction retour au menu principal
def start_the_game_retour():
    subprocess.Popen(["python", "Menu2.py"])

# Configuration de la surface d'affichage
DISPLAY_SIZE = (900, 600)
surface = pygame.display.set_mode(DISPLAY_SIZE)

# Initialisation de Pygame
pygame.init()

# Fonction pour définir le nombre de joueurs
def set_nb_player(value, player_index):
    global nb_player
    if player_index == 0:
        nb_player = 2
    elif player_index == 1:
        nb_player = 4

# Fonction pour définir la taille du tableau
def set_board_size(value, size_index):
    global NUM_CELLS
    if size_index == 0:
        NUM_CELLS = 5
    elif size_index == 1:
        NUM_CELLS = 7
    elif size_index == 2:
        NUM_CELLS = 9
    elif size_index == 3:
        NUM_CELLS = 11

def set_nb_barriere(value, barrier_index):
    global nb_barriere
    nb_barriere = (barrier_index * 4) + 4

def start_the_game(bool):
    MENU_SIZE = (900, 600)



    # Création du thème
    mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 95),
                                       title_background_color=(0, 0, 0, 50),
                                       title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                       widget_font_color=(255, 255, 255))

    menu = pygame_menu.Menu('Quoridor Game', *MENU_SIZE, theme=mytheme)

    # Ajout des éléments de menu
    DEFAULT_NAME = 'Pseudo '
    DEFAULT_NAME2 = 'Pseudo '
    menu.add.text_input('Player 1 :', default=DEFAULT_NAME, maxchar=15, font_size=28)
    menu.add.text_input('Player 2 :', default=DEFAULT_NAME2, maxchar=15, font_size=28)

    Player_choise = [('2 joueurs', 0), ('4 joueurs', 1)]
    Tableau = [('05X05', 0), ('07X07', 1), ('09X09', 2), ('11X11', 3)]
    Barriere = [(f'{i}', i // 4 - 1) for i in range(4, 41, 4)]

    menu.add.selector('Choisir Taille tableau  :', Tableau, onchange=set_board_size, font_size=28, default=2)
    menu.add.selector('Choisir de Nombre de joueurs  :', Player_choise, onchange=set_nb_player, font_size=28, default=0)
    menu.add.selector('Choisir le nombre de barrières :', Barriere, onchange=set_nb_barriere, font_size=28 , default=4)

    menu.add.button('Valider', lambda: validate_choices(bool), font_size=30)
    menu.add.button('Retour', start_the_game_retour)

    # Boucle principale du menu
    menu.mainloop(surface)


# Fonction pour valider les choix
def validate_choices(bool):
    pygame.display.quit()
    walls = [[{"TOP": 0, "BOTTOM": 0, "LEFT": 0, "RIGHT": 0} for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]
    board = [[0] * NUM_CELLS for _ in range(NUM_CELLS)]
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    BOARD_WIDTH = NUM_CELLS * CELL_SIZE
    BOARD_HEIGHT = NUM_CELLS * CELL_SIZE
    BOARD_LEFT = (screen_width - BOARD_WIDTH) // 2
    BOARD_TOP = (screen_height - BOARD_HEIGHT) // 2
    change_wall(NUM_CELLS,walls)
    player_in_game = Player.create_players(Player, nb_player, nb_barriere, NUM_CELLS)
    player_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
    
    while True:
        if not bool:
            connection = 0
            jeux(walls, screen, CELL_SIZE, BOARD_LEFT, BOARD_TOP, NUM_CELLS, player_in_game, player_color, board, nb_player, nb_barriere,connection)
        else:
            parametre = {
                'walls': walls,
                'screen': screen,
                'CELL_SIZE': CELL_SIZE,
                'BOARD_LEFT': BOARD_LEFT,
                'BOARD_TOP': BOARD_TOP,
                'NUM_CELLS': NUM_CELLS,
                'player_in_game': player_in_game,
                'player_color': player_color,
                'board': board,
                'nb_player': nb_player,
                'nb_barriere': nb_barriere,
            }

            connection = join_game("localhost")
            if 'screen' in parametre:
                del parametre['screen'] 
            envoyer_parametre_client_vers_server(connection, parametre)
            jeux(walls, screen, CELL_SIZE, BOARD_LEFT, BOARD_TOP, NUM_CELLS, player_in_game, player_color, board, nb_player, nb_barriere,connection)
        break


