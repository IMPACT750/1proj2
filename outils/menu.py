import pygame
import pygame.locals as pl
import subprocess

# Initialiser pygame
pygame.init()
pygame.mixer.init()  # Initialiser le mixer de Pygame pour la musique

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = WHITE

# Définir la taille de l'écran
screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)

# Charger la musique de fond
pygame.mixer.music.load("outils/song.mp3")  # Remplacez "votre_musique.mp3" par le nom de votre fichier audio

# Définir le fond d'écran
background_color = WHITE

# Définir la police et la taille du texte
font = pygame.font.Font(None, 36)

# Créer une surface pour le titre
title_text = "Le Quoridor Game"
title_surface = font.render(title_text, True, BLACK)
title_rect = title_surface.get_rect()
title_rect.centerx = screen.get_rect().centerx
title_rect.centery = screen.get_rect().centery - 200

# Créer les boutons
button_texts = ["Jouer en local", "Jouer en Réseau", "Jouer avec IA", "Règlement"]
button_surfaces = []
button_text_rects = []
button_rects = []
button_spacing = 80  # Espacement vertical entre les boutons

button_rect_x = screen.get_rect().centerx - 100  # Position x commune pour tous les boutons

for i in range(4):
    button_text_surface = font.render(button_texts[i], True, BUTTON_TEXT_COLOR)
    button_text_rect = button_text_surface.get_rect()
    button_text_rect.centerx = screen.get_rect().centerx
    button_text_rect.centery = screen.get_rect().centery + i * button_spacing
    button_rect = pygame.Rect(
        button_rect_x,
        button_text_rect.top - 10,
        200,
        button_text_rect.height + 20
    )

    button_surfaces.append(button_text_surface)
    button_text_rects.append(button_text_rect)
    button_rects.append(button_rect)

# Charger l'image du logo son
logo_image = pygame.image.load("outils/son.png")
logo_image_coupe = pygame.image.load("outils/son_coupe.png")
logo_image_original = pygame.transform.scale(logo_image, (50, 50))  # Image originale à la taille d'origine
logo_image = logo_image_original.copy()  # Copie de l'image originale pour redimensionnement
logo_image_coupe = pygame.transform.scale(logo_image_coupe, (50, 50))  # Redimensionner l'image du logo coupé
logo_rect = logo_image.get_rect()
logo_rect.topright = (screen.get_width() - 20, 20)  # Positionner le rectangle du logo en haut à droite de l'écran

# Variable de contrôle du son
mute = False  # Indique si le son est coupé ou non

# Boucle principale
done = False
pygame.mixer.music.play(-1)  # Jouer la musique en boucle

while not done:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pl.KEYDOWN:
            if event.key == pl.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si un bouton a été cliqué
            for i in range(4):
                if button_rects[i].collidepoint(event.pos):
                    if i == 0:  # Bouton "Jouer en local" cliqué
                        subprocess.run(["python", "Menujeux.py"])  # Execute the "main.py" file
                    elif i == 1:  # Bouton "Jouer en Réseau" cliqué
                        subprocess.run(["python", "1serveur.py"])  # Execute the "1serveur.py" file
                    elif i == 2: # Bouton "Jouer avec IA" cliqué
                        subprocess.run(["python", "ia.py"])
                    elif i == 3: # Bouton "Règlement" cliqué
                        subprocess.run(["python", "reglement.py"])
                    
            # Vérifier si le logo son a été cliqué
            if logo_rect.collidepoint(event.pos):
                mute = not mute  # Inverser l'état de coupure du son
                if mute:
                    pygame.mixer.music.pause()  # Couper la musique
                    logo_image = logo_image_coupe  # Changer l'image du logo
                else:
                    pygame.mixer.music.unpause()  # Réactiver la musique
                    logo_image = logo_image_original.copy()  # Recharger l'image du logo à la taille d'origine

    # Afficher le fond d'écran
    screen.fill(background_color)

    # Afficher le titre et les boutons
    screen.blit(title_surface, title_rect)
    for i in range(4):
        button_color = BUTTON_HOVER_COLOR if button_rects[i].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rects[i])
        screen.blit(button_surfaces[i], button_text_rects[i])

    # Afficher le logo son
    screen.blit(logo_image, logo_rect)

    # Mettre à jour l'écran
    pygame.display.flip()

# Arrêter la musique de fond et quitter pygame
pygame.mixer.music.stop()
pygame.quit()
