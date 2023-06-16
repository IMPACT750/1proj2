import pygame
import pygame_menu
import subprocess
from fonction_reseau import *
from main import *
ip= ""

CLIENT = 1
SERVER = 2
# Initialisation de Pygame
pygame.init()

# Configuration de la surface d'affichage
DISPLAY_SIZE = (1000, 800)
surface = pygame.display.set_mode(DISPLAY_SIZE)

# Fonction pour définir le nombre de joueurs
def set_players(value, players):
    print('Number of players selected: ', players)


# Fonction pour démarrer le jeu en mode IA
def start_the_game_retour():
    subprocess.Popen(["python", "Menu2.py"])

def validate_choices():
    ip = adresse_ip.get_value()
    connexion = join_game(ip)
    parametre = recevoir_parametre_client(connexion)
    while True:
        jeux(parametre['walls'],surface, parametre['CELL_SIZE'],parametre['BOARD_LEFT'],
             parametre['BOARD_TOP'], parametre['NUM_CELLS'],parametre['player_in_game'],
             parametre['player_color'],parametre['board'],parametre['nb_player'],parametre['nb_barriere'],
             connexion=connexion,id_client=parametre['id_client'])


# Configuration du menu
MENU_SIZE = (900, 600)
# Création du thème
mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 95),  # Couleur de fond semi-transparente
                                   title_background_color=(0, 0, 0, 50),  # Couleur de fond du titre semi-transparente
                                   title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                   widget_font_color=(255, 255, 255))  # Couleur de la police blanche

menu = pygame_menu.Menu('Quoridor Game', *MENU_SIZE, theme=mytheme)  # Utilisation du thème personnalisé

# Ajout des éléments de menu
adresse_ip = menu.add.text_input('Rentré adresse ip: ', default="")
menu.add.button('Valider', validate_choices, font_size=30)
menu.add.button('Retour', start_the_game_retour)

# Boucle principale du menu
if __name__ == "__main__":
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()