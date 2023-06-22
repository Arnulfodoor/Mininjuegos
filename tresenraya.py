import pygame
import sys

# Constantes del juego
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 6
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Constantes de los jugadores
MAX = 1
MIN = -1

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_board(tablero):
    screen.fill(BLACK)
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE), LINE_WIDTH)
            
            if tablero[row * BOARD_SIZE + col] == MAX:
                pygame.draw.circle(screen, WHITE, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10, LINE_WIDTH)
            elif tablero[row * BOARD_SIZE + col] == MIN:
                pygame.draw.line(screen, WHITE, (x + 10, y + 10), (x + SQUARE_SIZE - 10, y + SQUARE_SIZE - 10), LINE_WIDTH)
                pygame.draw.line(screen, WHITE, (x + SQUARE_SIZE - 10, y + 10), (x + 10, y + SQUARE_SIZE - 10), LINE_WIDTH)
    
    pygame.display.flip()

def minimax(tablero, jugador):
    if game_over(tablero):
        return [ganador(tablero), None]
    
    movimientos = []
    
    for i in range(len(tablero)):
        if tablero[i] == 0:
            tableroaux = tablero[:]
            tableroaux[i] = jugador
            puntuacion = minimax(tableroaux, jugador * (-1))
            movimientos.append([puntuacion[0], i])
    
    if jugador == MAX:
        movimiento = max(movimientos)
    else:
        movimiento = min(movimientos)
    
    return movimiento

def game_over(tablero):
    return ganador(tablero) != 0 or 0 not in tablero

def ganador(tablero):
    lineas_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]  # Diagonales
    ]
    
    for linea in lineas_ganadoras:
        if tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] != 0:
            return tablero[linea[0]]
    
    return 0

def juega_humano(tablero):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // SQUARE_SIZE
                col = mouse_pos[0] // SQUARE_SIZE
                index = row * BOARD_SIZE + col
                if tablero[index] == 0:
                    tablero[index] = MIN
                    return tablero

def juega_ordenador(tablero):
    punt = minimax(tablero[:], MAX)
    tablero[punt[1]] = MAX
    return tablero

def reiniciar_juego():
    return [0, 0, 0, 0, 0, 0, 0, 0, 0]

# Resto del código...

if __name__ == "__main__":
    # Inicialización de variables y tablero
    tablero = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw_board(tablero)
        
        if not game_over(tablero):
            tablero = juega_humano(tablero)
            if not game_over(tablero):
                tablero = juega_ordenador(tablero)
        else:
            # El juego ha terminado, reiniciar el tablero
            tablero = reiniciar_juego()
            draw_board(tablero)
            # Determinar el ganador y mostrarlo
            g = ganador(tablero)
            if g == 0:
                gana = 'Empate'
            elif g == MIN:
                gana = 'Jugador'
            else:
                gana = 'Ordenador'
            print('Ganador: ' + gana)
