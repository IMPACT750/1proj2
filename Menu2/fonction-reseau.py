import time
import threading
import socket
import pygame_menu
import pygame
from main import *
from Players import Player
from Menujeux import *

class ThreadforClient(threading.Thread):

    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.lock = threading.Lock()

    def envoyer_tableau_jeu(self, tableau_joueur):
        self.lock.acquire()
        self.connexion.sendall(str(tableau_joueur).encode("utf-8"))
        self.lock.release()

    def envoyer_tableau_walls(self, tableau_walls):
        self.lock.acquire()
        self.connexion.sendall(str(tableau_walls).encode("utf-8"))
        self.lock.release()

    def recevoir_tableau_jeu(self):
        self.lock.acquire()
        tableau_joueur = self.connexion.recv(1024).decode()
        self.lock.release()
        return tableau_joueur

    def recevoir_tableau_walls(self):
        self.lock.acquire()
        tableau_walls = self.connexion.recv(1024).decode()
        self.lock.release()
        return tableau_walls


def host_game():
    # Création de la socket
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.bind(('', 12800))
    connexion.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(12800))

    # Attente d'un client
    connexion_avec_client, infos_connexion = connexion.accept()

    # Création du thème
    mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 95),
                                       title_background_color=(0, 0, 0, 50),
                                       title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                       widget_font_color=(255, 255, 255))

    # Configuration de la surface d'affichage
    DISPLAY_SIZE = (900, 600)
    surface = pygame.display.set_mode(DISPLAY_SIZE)

    # Initialisation de Pygame
    pygame.init()

    # Variable globale
    CELL_SIZE = 50
    NUM_CELLS = 9
    nb_player = 2
    nb_barriere = 20

    # Création du menu
    MENU_SIZE = (900, 600)
    menu = pygame_menu.Menu('Quoridor Game', *MENU_SIZE, theme=mytheme)

    # Ajout des éléments de menu
    DEFAULT_NAME = 'Pseudo '
    DEFAULT_NAME2 = 'Pseudo '
    menu.add.text_input('Player 1 :', default=DEFAULT_NAME, maxchar=15, font_size=28)
    menu.add.text_input('Player 2 :', default=DEFAULT_NAME2, maxchar=15, font_size=28)

    Player_choise = [('2 joueurs', 0), ('4 joueurs', 1)]
    menu.add.selector('Nombre de joueurs :', Player_choise, onchange=set_nb_player)
    Board_choise = [('5x5', 0), ('7x7', 1), ('9x9', 2), ('11x11', 3)]
    menu.add.selector('Taille du plateau :', Board_choise, onchange=set_board_size)
    Barrier_choise = [('4', 0), ('8', 1), ('12', 2), ('16', 3)]
    menu.add.selector('Nombre de barrières :', Barrier_choise)
