import tkinter as tk
from tkinter import messagebox

def show_barrier_dialog():
    value = barrier_entry.get()
    if value.isdigit() and 4 <= int(value) <= 40:
        messagebox.showinfo("Nombre de barrières", f"Vous avez choisi {value} barrières.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide entre 4 et 40.")

def create_buttons_frame(root, texts, commands):
    frame = tk.Frame(root)
    for text, command in zip(texts, commands):
        button = tk.Button(frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)
    frame.pack()


def on_5x5_click():
    value = 5
    return value


def on_7x7_click():
    value = 7
    return value

def on_9x9_click():
    value = 9
    return value

def on_11x11_click():
    value = 11
    return value

def on_2_players_click():
    value = 2
    return value

def on_4_players_click():
    value = 4
    return value



root = tk.Tk()
root.title("Quoridor Dame")

root.geometry("800x800")  # Définir la taille de la fenêtre (largeur x hauteur)

barrier_label = tk.Label(root, text="Choisissez taille de tableau:")
barrier_label.pack(pady=5)

def yorel():
    if evl[0]=="5x5":
      print(5)
      valeur=5
      print(valeur)
    return valeur

evl=["5x5", "7x7", "9x9", "11x11"]


# Création des boutons 5x5, 7x7, 9x9 et 11x11
button_frame1 = tk.Frame(root)
create_buttons_frame(button_frame1, [evl],[yorel])
button_frame1.pack(pady=10)


barrier_label = tk.Label(root, text="Choisissez le nombre de Joueurs (entre 2 et 4):")
barrier_label.pack(pady=5)
# Création des boutons 2 joueurs et 4 joueurs
button_frame2 = tk.Frame(root)
create_buttons_frame(button_frame2, ["2 joueurs", "4 joueurs"], [on_2_players_click, on_4_players_click])
button_frame2.pack(pady=10)

# Création de la zone de texte pour choisir le nombre de barrières
barrier_label = tk.Label(root, text="Choisissez le nombre de barrières (entre 4 et 40):")
barrier_label.pack(pady=5)

barrier_entry = tk.Entry(root)
barrier_entry.pack(pady=5)

# Création du bouton pour choisir le nombre de barrières
barrier_button = tk.Button(root, text="Valider", command=show_barrier_dialog)
barrier_button.pack(pady=5)

root.mainloop()
