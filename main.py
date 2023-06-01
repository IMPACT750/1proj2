import tkinter as tk
from sous_menu import *
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
        self.title("Hello World")
        self.geometry("1000x1000")
        self.configure(bg="black")  # Définition de la couleur de fond en noir
        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.tableau = []

    def creer_tableau(self, taille):
        for i in range(taille):
            self.tableau.append([])
            for j in range(taille):
                if get_value_joueur() == 2:
                    if i == taille//2 and j == 0:
                        self.tableau[i].append(JOUEUR1)
                    elif i == taille//2 and j == taille-1:
                        self.tableau[i].append(JOUEUR2)
                    else:
                        self.tableau[i].append(0)
                elif get_value_joueur() == 4:
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
                if (i+j)%2 == 0:
                    self.canvas.create_rectangle(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill="white")
                else:
                    self.canvas.create_rectangle(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill="grey")
                if tableau[i][j] == 1:
                    self.canvas.create_oval(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill=COULEUR_JOUEUR1)
                elif tableau[i][j] == 2:
                    self.canvas.create_oval(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill=COULEUR_JOUEUR2)
                elif tableau[i][j] == 3:
                    self.canvas.create_oval(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill=COULEUR_JOUEUR3)
                elif tableau[i][j] == 4:
                    self.canvas.create_oval(i*TAILLE_CELLULE, j*TAILLE_CELLULE, i*TAILLE_CELLULE+TAILLE_CELLULE, j*TAILLE_CELLULE+TAILLE_CELLULE, fill=COULEUR_JOUEUR4)


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




app = App()
tableau = app.creer_tableau(11)
app.dessiner_tableau(tableau)
app.mainloop()
