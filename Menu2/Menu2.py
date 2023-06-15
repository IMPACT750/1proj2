import pygame
import pygame_menu
import subprocess

# Initialisation de Pygame
pygame.init()

# Configuration de la surface d'affichage
DISPLAY_SIZE = (900, 600)
surface = pygame.display.set_mode(DISPLAY_SIZE)

# Fonction pour définir le nombre de joueurs
def set_players(value, players):
    print('Number of players selected: ', players)

# Fonction pour démarrer le jeu en mode local
def start_the_game_local():
    subprocess.Popen(["python", "Menujeux.py"])


# Fonction pour démarrer le jeu en mode IA
def start_the_game_IA():
    subprocess.Popen(["python", "ia.py"])

# Fonction pour démarrer le jeu en mode réseau
def start_the_game_network():
    print('Starting the game in network mode')

# Configuration du menu
MENU_SIZE = (900, 600)

# Création du thème
mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 95),  # Couleur de fond semi-transparente
                                   title_background_color=(0, 0, 0, 50),  # Couleur de fond du titre semi-transparente
                                   title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                   widget_font_color=(255, 255, 255))  # Couleur de la police blanche

menu = pygame_menu.Menu('Quoridor Game', *MENU_SIZE, theme=mytheme)  # Utilisation du thème personnalisé

# Ajout des éléments de menu
menu.add.button('Play Local', start_the_game_local)
menu.add.button('Play IA', start_the_game_IA)
menu.add.button('Play Réseau', start_the_game_network)
menu.add.button('Quit', pygame_menu.events.EXIT)

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
