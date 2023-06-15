import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (30, 144, 255)

# Définition des dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Règlement du jeu Quoridor")

# Chargement du règlement du jeu
reglement = [
    "Règles du jeu Quoridor:",
    "Le jeu Quoridor se joue sur un plateau de 9x9 cases.",
    "Chaque joueur possède un pion qu'il peut déplacer d'une case à la fois.",
    "L'objectif du jeu est d'atteindre la ligne opposée du plateau avec son pion.",
    "Les joueurs peuvent également placer des barrières pour bloquer le passage de l'adversaire.",
    "Chaque joueur dispose de 10 barrières qu'il peut placer verticalement ou horizontalement.",
    "Les barrières ne peuvent pas être déplacées une fois qu'elles sont placées.",
    "Le joueur peut sauter par-dessus une barrière si celle-ci est adjacente à son pion.",
    "Le joueur ne peut pas sauter par-dessus une barrière si celle-ci est adjacente à un autre pion.",
    "Le jeu se termine lorsqu'un joueur atteint la ligne opposée avec son pion, ou lorsque l'autre joueur ne peut plus se déplacer.",
    "Le joueur qui atteint la ligne opposée en premier remporte la partie."
]

# Définition des polices d'écriture
police_titre = pygame.font.SysFont("Arial", 36, bold=True)
police_texte = pygame.font.SysFont("Arial", 24)

# Boucle principale du jeu
def afficher_reglement():
    fenetre.fill(BLANC)

    # Affichage du titre
    titre = police_titre.render("Règlement du jeu Quoridor", True, NOIR)
    rect_titre = titre.get_rect(center=(largeur_fenetre // 2, 50))
    fenetre.blit(titre, rect_titre)

    # Affichage du règlement
    y = 120
    for ligne in reglement:
        texte = police_texte.render(ligne, True, NOIR)
        rect = texte.get_rect(center=(largeur_fenetre // 2, y))
        fenetre.blit(texte, rect)
        y += 30

    # Affichage du bouton de fermeture
    pygame.draw.rect(fenetre, BLEU, (largeur_fenetre - 80, 10, 70, 30))
    texte_bouton = police_texte.render("Fermer", True, BLANC)
    rect_bouton = texte_bouton.get_rect(center=(largeur_fenetre - 40, 25))
    fenetre.blit(texte_bouton, rect_bouton)

    pygame.display.flip()

# Boucle principale du programme
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect_bouton.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    afficher_reglement()
