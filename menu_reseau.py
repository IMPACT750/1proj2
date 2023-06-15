import pygame
import pygame_menu
import subprocess
import Menujeux

# Initialisation de Pygame
pygame.init()

# Configuration de la surface d'affichage
DISPLAY_SIZE = (900, 600)
surface = pygame.display.set_mode(DISPLAY_SIZE)



# Fonction pour démarrer le jeu en mode local
def start_the_game_host():
    Menujeux.start_the_game(True)

# Fonction pour démarrer le jeu en mode IA
def start_the_game_rejoined_parti():
    subprocess.Popen(["python", "menu_rejoindre_partit.py"])



# Menu variable
menu = None


def start_the_game():
    global menu  # We declare menu as a global variable
    # Configuration du menu
    MENU_SIZE = (900, 600)

    # Création du thème
    mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 95),  # Couleur de fond semi-transparente
                                       title_background_color=(0, 0, 0, 50),
                                       # Couleur de fond du titre semi-transparente
                                       title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                                       widget_font_color=(255, 255, 255))  # Couleur de la police blanche

    menu = pygame_menu.Menu('Quoridor Game', *MENU_SIZE, theme=mytheme)  # Utilisation du thème personnalisé

    # Ajout des éléments de menu
    menu.add.button('Host', start_the_game_host)
    menu.add.button('Rejoindre Parti', start_the_game_rejoined_parti)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Boucle principale du menu
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()


if __name__ == "__main__":
    start_the_game()
