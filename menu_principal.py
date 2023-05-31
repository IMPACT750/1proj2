import tkinter as tk
from tkinter import ttk
import subprocess
import pygame

def jouer_en_local():
    subprocess.run(["python", "fichier_jouer_local.py"])

def jouer_contre_ordi():
    subprocess.run(["python", "fichier_jouer_ordi.py"])

def jouer_en_ligne():
    subprocess.run(["python", "fichier_jouer_ligne.py"])

def a_propos():
    subprocess.run(["python", "fichier_a_propos.py"])

def jouer_musique():
    pygame.mixer.music.load("Menu Principal/song.mp3")
    pygame.mixer.music.play()

def arreter_musique():
    pygame.mixer.music.stop()

def changer_logo():
    global logo_image
    if logo_image == logo_image1:
        logo_label.config(image=logo_image2)
        logo_image = logo_image2
    else:
        logo_label.config(image=logo_image1)
        logo_image = logo_image1

pygame.init()

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry("800x800")  # Changer la taille de la fenêtre ici

# Création du titre
titre = tk.Label(fenetre, text="Menu Principal", font=("Helvetica", 16, "bold"))
titre.pack(side="top", pady=20)

# Création du conteneur pour le logo
conteneur_logo = tk.Frame(fenetre)
conteneur_logo.pack(side="top", padx=10, pady=10)

# Chargement des images du haut-parleur avec un facteur de réduction de 2
logo_image1 = tk.PhotoImage(file="Menu Principal/haut-parleur.png").subsample(11)
logo_image2 = tk.PhotoImage(file="Menu Principal/haut-parleur-barre.png").subsample(11)

# Création du widget Label pour afficher le logo
logo_image = logo_image1  # Définir l'image initiale
logo_label = tk.Label(conteneur_logo, image=logo_image)
logo_label.pack(pady=(0, 10))  # Ajouter un espace de 10 pixels en bas pour le décalage

# Lier l'événement de clic sur le label du logo aux fonctions arreter_musique et changer_logo
logo_label.bind("<Button-1>", lambda event: [arreter_musique(), changer_logo()])

# Création du conteneur au centre de la fenêtre
conteneur_centre = tk.Frame(fenetre)
conteneur_centre.pack(expand=True)

# Création des styles de boutons
style = ttk.Style()
style.configure("TButton",
                foreground="black",
                background="lightgray",
                font=("Helvetica", 12, "bold"),
                padding=10)
style.configure("TButton", width=15)  # Changer la largeur des boutons ici

# Création du bouton et placement dans le conteneur au centre
bouton_local = ttk.Button(conteneur_centre, text="Jouer en local", command=jouer_en_local, style="TButton")
bouton_local.pack(pady=10)

# Création des autres boutons (à ajuster selon vos préférences)
bouton_ordi = ttk.Button(conteneur_centre, text="Jouer contre AI", command=jouer_contre_ordi, style="TButton")
bouton_ordi.pack(pady=10)

bouton_ligne = ttk.Button(conteneur_centre, text="Jouer en ligne", command=jouer_en_ligne, style="TButton")
bouton_ligne.pack(pady=10)

bouton_apropos = ttk.Button(conteneur_centre, text="À propos", command=a_propos, style="TButton")
bouton_apropos.pack(pady=10)

# Lancement de la musique
jouer_musique()

# Lancement de la boucle principale
fenetre.mainloop()

pygame.mixer.music.stop()
pygame.quit()
