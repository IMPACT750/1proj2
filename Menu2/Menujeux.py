import pygame
import pygame_menu
from main import *
from Players import Player

# Variable globale
CELL_SIZE = 50
NUM_CELLS = 9
nb_player = 2
nb_barriere = 20

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

def start_the_game():
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


    menu.add.button('Valider', validate_choices, font_size=30)
    menu.add.button('Retour', pygame_menu.events.EXIT, font_size=30)

    # Boucle principale du menu
    menu.mainloop(surface)

# Fonction pour valider les choix
def validate_choices():
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

    player1 = Player(NUM_CELLS // 2, 0,nb_barriere//nb_player, 1)
    player2 = Player(NUM_CELLS // 2, NUM_CELLS - 1,nb_barriere//nb_player, 2)
    player3 = Player(0, NUM_CELLS // 2,nb_barriere//nb_player, 3)
    player4 = Player(NUM_CELLS - 1, NUM_CELLS // 2,nb_barriere//nb_player,4)
    player_in_game = [player1, player2, player3, player4]
    player_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
    draw_board(NUM_CELLS, screen, BOARD_LEFT, CELL_SIZE, BOARD_TOP)
    create_player(nb_player, BOARD_LEFT, BOARD_TOP, CELL_SIZE, player_in_game, player_color, screen, board)
    while True:
        jeux(walls, screen, CELL_SIZE, BOARD_LEFT, BOARD_TOP, NUM_CELLS, player_in_game, player_color, board, nb_player, nb_barriere)

start_the_game()

