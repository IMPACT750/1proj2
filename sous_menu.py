import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def refresh_page():
    root.update()  # Update the root window
    root.after(1000, refresh_page)  # Schedule the refresh_page function to be called after 1 second

def show_barrier_dialog():
    value = barrier_entry.get()
    if value.isdigit() and 4 <= int(value) <= 40:
        messagebox.showinfo("Nombre de barrières", f"Vous avez choisi {value} barrières.")
        start_timer()
    else:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide entre 4 et 40.")

def create_buttons_frame(root, texts, commands):
    frame = tk.Frame(root)
    for text, command in zip(texts, commands):
        button = tk.Button(frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)
    frame.pack()



def on_button_click(value):
    global value_taille_tableau
    if value in [5, 7, 9, 11]:
        value_taille_tableau = value
    return value_taille_tableau
    

def get_value_joueur(value):
    global value_joueur
    if value in [2, 4]:
        value_joueur = value
    return value_joueur

def reset_game():
    barrier_entry.delete(0, tk.END)

def start_timer():
    global start_time
    start_time = datetime.now()
    print("Chronomètre démarré.")
    update_timer()

def update_timer():
    elapsed_time = datetime.now() - start_time
    timer_label.configure(text=str(elapsed_time))
    timer_label.after(1000, update_timer)  # Update the timer every second (1000 milliseconds)

root = tk.Tk()
root.title("Quoridor Dame")
root.geometry("800x800")

barrier_label = tk.Label(root, text="Choisissez taille de tableau:")
barrier_label.pack(pady=5)

button_frame1 = tk.Frame(root)
create_buttons_frame(button_frame1, ["5x5", "7x7", "9x9", "11x11"], [lambda: on_button_click(5), lambda: on_button_click(7), lambda: on_button_click(9), lambda: on_button_click(11)])
button_frame1.pack(pady=10)

barrier_label = tk.Label(root, text="Choisissez le nombre de Joueurs (entre 2 et 4):")
barrier_label.pack(pady=5)

button_frame2 = tk.Frame(root)
create_buttons_frame(button_frame2, ["2 joueurs", "4 joueurs"], [lambda: get_value_joueur(2), lambda: get_value_joueur(4)])
button_frame2.pack(pady=10)

barrier_label = tk.Label(root, text="Choisissez le nombre de barrières (entre 4 et 40):")
barrier_label.pack(pady=5)

barrier_entry = tk.Entry(root)
barrier_entry.pack(pady=5)

barrier_button = tk.Button(root, text="Valider", command=show_barrier_dialog)
barrier_button.pack(pady=5)

reset_button = tk.Button(root, text="Réinitialiser", command=reset_game)
reset_button.pack(pady=5)

# Create a label to display the timer
timer_label = tk.Label(root, text="00:00:00", font=("Arial", 24))
timer_label.pack(pady=10)

refresh_page()
root.mainloop()
