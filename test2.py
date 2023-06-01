import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess

TAILLE_CELLULE = 50
JOUEUR1 = 1
JOUEUR2 = 2
JOUEUR3 = 3
JOUEUR4 = 4
COULEUR_JOUEUR1 = "red"
COULEUR_JOUEUR2 = "blue"
COULEUR_JOUEUR3 = "green"
COULEUR_JOUEUR4 = "yellow"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quoridor Dame")
        self.geometry("800x800")

        self.barrier_label1 = tk.Label(self, text="Choisissez la taille du tableau:")
        self.barrier_label1.pack(pady=5)

        self.button_frame1 = tk.Frame(self)
        self.create_buttons_frame(self.button_frame1, ["5x5", "7x7", "9x9", "11x11"],
                                  [lambda: self.on_button_click(5), lambda: self.on_button_click(7),
                                   lambda: self.on_button_click(9), lambda: self.on_button_click(11)])
        self.button_frame1.pack(pady=10)

        self.barrier_label2 = tk.Label(self, text="Choisissez le nombre de joueurs (entre 2 et 4):")
        self.barrier_label2.pack(pady=5)

        self.button_frame2 = tk.Frame(self)
        self.create_buttons_frame(self.button_frame2, ["2 joueurs", "4 joueurs"],
                                  [lambda: self.get_value_joueur(2), lambda: self.get_value_joueur(4)])
        self.button_frame2.pack(pady=10)

        self.barrier_label3 = tk.Label(self, text="Choisissez le nombre de barrières (entre 4 et 40):")
        self.barrier_label3.pack(pady=5)

        self.barrier_entry = tk.Entry(self)
        self.barrier_entry.pack(pady=5)

        self.barrier_button = tk.Button(self, text="Valider", command=self.show_barrier_dialog)
        self.barrier_button.pack(pady=5)

        self.reset_button = tk.Button(self, text="Réinitialiser", command=self.reset_game)
        self.reset_button.pack(pady=5)

        # Créer une étiquette pour afficher le chronomètre
        self.timer_label = tk.Label(self, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        self.save_button = tk.Button(self, text="Enregistrer & arrêter le jeu", command=self.save_and_open_main)
        self.save_button.pack(pady=5)

        self.canvas = tk.Canvas(self)
        self.tableau = []

    def create_buttons_frame(self, root, texts, commands):
        for text, command in zip(texts, commands):
            button = tk.Button(root, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_button_click(self, value):
        if value in [5, 7, 9, 11]:
            self.value_taille_tableau = value

    def get_value_joueur(self, value):
        if value in [2, 4]:
            self.value_joueur = value

    def reset_game(self):
        self.barrier_entry.delete(0, tk.END)

    def start_timer(self):
        self.start_time = datetime.now()
        print("Chronomètre démarré.")
        self.update_timer()

    def update_timer(self):
        elapsed_time = datetime.now() - self.start_time
        self.timer_label.configure(text=str(elapsed_time))
        self.timer_label.after(1000, self.update_timer)  # Mettre à jour le timer toutes les secondes (1000 millisecondes)

    def show_barrier_dialog(self):
        value = self.barrier_entry.get()
        if value.isdigit() and 4 <= int(value) <= 40:
            messagebox.showinfo("Nombre de barrières", f"Vous avez choisi {value} barrières.")
            self.start_timer()
            self.subprocess = subprocess.run(["python", "main.py"])  # Ouvre la page main.py
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide entre 4 et 40.")

    def creer_tableau(self, taille):
        for i in range(taille):
            self.tableau.append([])
            for j in range(taille):
                if  self.value_joueur == 2:
                    if i == taille//2 and j == 0:
                        self.tableau[i].append(JOUEUR1)
                    elif i == taille//2 and j == taille-1:
                        self.tableau[i].append(JOUEUR2)
                    else:
                        self.tableau[i].append(0)
                elif  self.value_joueurr == 4:
                    if i == 0 and j == 0:
                        self.tableau[i].append(JOUEUR1)
                    elif i == 0 and j == taille-1:
                        self.tableau[i].append(JOUEUR2)
                    elif i == taille-1 and j == 0:
                        self.tableau[i].append(JOUEUR3)
                    elif i == taille-1 and j == taille-1:
                        self.tableau[i].append(JOUEUR4)
                    else:
                        self.tableau[i].append(0)
        print(self.tableau)
        return self.tableau

    def dessiner_tableau(self, tableau):
        self.canvas.delete("all")

        canvas_width = len(tableau) * TAILLE_CELLULE
        canvas_height = len(tableau[0]) * TAILLE_CELLULE

        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        canvas_x = (parent_width - canvas_width) // 2
        canvas_y = (parent_height - canvas_height) // 2

        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.config(width=canvas_width, height=canvas_height)

        for i in range(len(tableau)):
            for j in range(len(tableau[i])):
                if (i + j) % 2 == 0:
                    self.canvas.create_rectangle(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                                 i * TAILLE_CELLULE + TAILLE_CELLULE,
                                                 j * TAILLE_CELLULE + TAILLE_CELLULE, fill="white")
                else:
                    self.canvas.create_rectangle(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                                 i * TAILLE_CELLULE + TAILLE_CELLULE,
                                                 j * TAILLE_CELLULE + TAILLE_CELLULE, fill="grey")
                if tableau[i][j] == 1:
                    self.canvas.create_oval(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                            i * TAILLE_CELLULE + TAILLE_CELLULE,
                                            j * TAILLE_CELLULE + TAILLE_CELLULE, fill=COULEUR_JOUEUR1)
                elif tableau[i][j] == 2:
                    self.canvas.create_oval(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                            i * TAILLE_CELLULE + TAILLE_CELLULE,
                                            j * TAILLE_CELLULE + TAILLE_CELLULE, fill=COULEUR_JOUEUR2)
                elif tableau[i][j] == 3:
                    self.canvas.create_oval(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                            i * TAILLE_CELLULE + TAILLE_CELLULE,
                                            j * TAILLE_CELLULE + TAILLE_CELLULE, fill=COULEUR_JOUEUR3)
                elif tableau[i][j] == 4:
                    self.canvas.create_oval(i * TAILLE_CELLULE, j * TAILLE_CELLULE,
                                            i * TAILLE_CELLULE + TAILLE_CELLULE,
                                            j * TAILLE_CELLULE + TAILLE_CELLULE, fill=COULEUR_JOUEUR4)

    def save_and_open_main(self):
        self.subprocess.kill()  # Arrête le processus du fichier main.py
        self.destroy()  # Ferme la fenêtre
    

class Player:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.numero = num
        self.num_walls = 10

    def deplacement(self, event, tableau):
        souris_x = event.x
        souris_y = event.y
        souris_x = souris_x // TAILLE_CELLULE
        souris_y = souris_y // TAILLE_CELLULE
        if (abs(souris_x - self.x) <= 1 and souris_y == self.y) or (abs(souris_y - self.y) <= 1 and souris_x == self.x):
            if self.check_collision(event,tableau):
                tableau[self.x][self.y] = 0
                self.x = souris_x
                self.y = souris_y
                tableau[self.x][self.y] = self.numero
                return tableau
            else:
                if self.x == souris_x and self.y != souris_y:
                    if self.y > souris_y:
                        if self.check_collision(event,tableau):
                            tableau[self.x][self.y] = 0
                            self.y -= 2
                            tableau[self.x][self.y] = self.numero
                            return tableau
                    else:
                        if self.check_collision(event,tableau):
                            tableau[self.x][self.y] = 0
                            self.y += 2
                            tableau[self.x][self.y] = self.numero
                            return tableau
                elif self.y == souris_y and self.x != souris_x:
                    if self.x > souris_x:
                        if self.check_collision(event,tableau):
                            tableau[self.x][self.y] = 0
                            self.x -= 2
                            tableau[self.x][self.y] = self.numero
                            return tableau
                    else:
                        if self.check_collision(event,tableau):
                            tableau[self.x][self.y] = 0
                            self.x += 2
                            tableau[self.x][self.y] = self.numero
                            return tableau
                else:
                    print("Déplacement impossible, vous avez cliquer sur votre case")
                    return tableau

    def check_collision(self,event, tableau):
        souris_x = event.x
        souris_y = event.y
        souris_x = souris_x // TAILLE_CELLULE
        souris_y = souris_y // TAILLE_CELLULE
        if tableau[souris_x][souris_y] == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    app = App()
    app.mainloop()
