import pygame
import socket 
import time
import threading

class ThreadforClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.lock = threading.Lock()


    def recevoir_des_donnees(self):
        with self.lock:
            data = self.conn.recv(1024).decode()
        if data:
            coords = data.split(',')
            print(coords,"recu")
            x1 = int(coords[0])
            y1 = int(coords[1])
            x2 = int(coords[2])
            y2 = int(coords[3])
            player1.x = x1
            player1.y = y1
            player2.x = x2
            player2.y = y2
            return True
        else:
            return False

    def run(self):
        while True:
            if self.recevoir_des_donnees():
                time.sleep(0.1)
            else:
                break



def envoyer_des_donnees():
    message = f"{player1.x},{player1.y},{player2.x},{player2.y}"
    socket.sendall(message.encode('utf-8'))
    print(message)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn, adress = ('localhost',5566)

socket.connect((conn, adress))


# Initialisation de Pygame

pygame.init()


# Définition de la taille de la fenêtre
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Définition des couleurs
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Définition des constantes du jeu
CELL_SIZE = 50
NUM_CELLS = 9
BOARD_WIDTH = NUM_CELLS * CELL_SIZE
BOARD_HEIGHT = NUM_CELLS * CELL_SIZE
BOARD_LEFT = (screen_width - BOARD_WIDTH) // 2
BOARD_TOP = (screen_height - BOARD_HEIGHT) // 2

# Définition de la classe Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_walls = 10

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

# Initialisation des joueurs
player1 = Player(4, 0)
player2 = Player(4, 8)

# Dessin des cases vides sur le plateau de jeu
def draw_board():
    for i in range(NUM_CELLS):
        for j in range(NUM_CELLS):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white, (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, gray, (BOARD_LEFT + i * CELL_SIZE, BOARD_TOP + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Dessin des joueurs
def draw_players():
    pygame.draw.circle(screen, (255, 0, 0), (BOARD_LEFT + player1.x * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP + player1.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
    pygame.draw.circle(screen, (0, 0, 255), (BOARD_LEFT + player2.x * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP + player2.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

# Actualisation de la fenêtre
pygame.display.flip()
# Boucle principale du jeu
# Boucle principale du jeu


while True:
    moved = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.move_up()
                moved = True
            elif event.key == pygame.K_DOWN:
                player1.move_down()
                moved = True
            elif event.key == pygame.K_LEFT:
                player1.move_left()
                moved = True
            elif event.key == pygame.K_RIGHT:
                player1.move_right()
                moved = True

    if moved:
        envoyer_des_donnees()
        
    ThreadforClient(socket).start()
    # Redessin du plateau
    screen.fill(black)
    draw_board()
    draw_players()
    pygame.display.update()

    # Redessin du plateau de
    # Effacement de l'écran
    screen.fill(black)

    # Dessin du plateau de jeu et des joueurs

    draw_board()
    draw_players()

    # Actualisation de la fenêtre
    pygame.display.update()
    time.sleep(0.1)


