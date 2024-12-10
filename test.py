from pynput import keyboard
import os

# Définir les couleurs des joueurs
COLOR_CODES = {
    "blue": '\033[34m',    # Bleu
    "yellow": '\033[33m',  # Jaune
    "red": '\033[31m',     # Rouge
    "green": '\033[32m',   # Vert
    "reset": '\033[0m'     # Réinitialiser la couleur
}

# Modèle des pièces du jeu
def generate_piece_model():
    return [
        [[1]],  # 1 carré
        [[1, 1]],  # 2 carrés
        [[1, 1, 1]],  # 3 carrés en ligne
        [[1], [1], [1]],  # 3 carrés en colonne
        [[1, 1, 0], [0, 1, 1]],  # 3 carrés en "L"
        [[1, 1, 1, 1]],  # 4 carrés en ligne
        [[1], [1], [1], [1]],  # 4 carrés en colonne
        [[1, 1], [1, 1]],  # 4 carrés en carré
        [[1, 1, 1], [0, 1, 0]],  # 4 carrés en "T"
        [[1, 1, 0], [0, 1, 1]],  # 4 carrés en "Z"
        [[1, 0, 0], [1, 1, 1]],  # 4 carrés en "L"
        [[1, 1, 1, 1, 1]],  # 5 carrés en ligne
        [[1], [1], [1], [1], [1]],  # 5 carrés en colonne
        [[1, 1, 1, 0], [0, 0, 1, 1]],  # 5 carrés en "Z" large
        [[1, 1, 1], [1, 0, 1]],  # 5 carrés en "T"
        [[1, 0, 0], [1, 1, 1], [0, 0, 1]],  # 5 carrés en "S"
        [[1, 0, 0], [1, 1, 1], [1, 0, 0]],  # 5 carrés en croix
        [[1, 1], [1, 0], [1, 1]],  # 5 carrés en "U"
        [[1, 1, 0], [1, 1, 1]],  # 5 carrés en "W"
        [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # 5 carrés en "T" décalé
        [[1, 1, 1], [1, 0, 0], [1, 0, 0]],  # 5 carrés en "L" large
    ]

# Génère les pièces pour chaque joueur
def generate_pieces():
    piece_model = generate_piece_model()
    return {
        "blue": [[[1 if cell else 0 for cell in row] for row in piece] for piece in piece_model],
        "yellow": [[[1 if cell else 0 for cell in row] for row in piece] for piece in piece_model],
        "red": [[[1 if cell else 0 for cell in row] for row in piece] for piece in piece_model],
        "green": [[[1 if cell else 0 for cell in row] for row in piece] for piece in piece_model],
    }

# Convertit un index en coordonnée (ligne ou colonne)
def index_to_coordinate(index):
    if index < 10:
        return str(index)
    return chr(index - 10 + ord("A"))

# Affiche le plateau de jeu
def display_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoie l'écran
    print("   " + "  ".join(str(i).rjust(2) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(f"{i:2} " + " ".join(f"{COLOR_CODES[cell]}■{COLOR_CODES['reset']}" if cell in COLOR_CODES else "." for cell in row))

# Prévisualisation de la pièce sur le plateau
def preview_piece(board, piece, x, y, player_color):
    board_copy = [row[:] for row in board]
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 1:
                if 0 <= x + i < len(board) and 0 <= y + j < len(board[0]):
                    board_copy[x + i][y + j] = player_color
    display_board(board_copy)

# Simulation interactive du placement d'une pièce
def simulate_placement(board, piece, player_color):
    x, y = 0, 0  # Position initiale
    direction = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    placement_confirmed = False
    cancelled = False

    def on_press(key):
        nonlocal x, y, placement_confirmed, cancelled
        if hasattr(key, 'name') and key.name in direction:
            dx, dy = direction[key.name]
            x = max(0, min(len(board) - len(piece), x + dx))
            y = max(0, min(len(board[0]) - len(piece[0]), y + dy))
        elif hasattr(key, 'name') and key.name == "enter":
            placement_confirmed = True
            return False  # Quitte le Listener
        elif hasattr(key, 'name') and key.name == "esc":
            cancelled = True
            return False  # Quitte le Listener

    with keyboard.Listener(on_press=on_press) as listener:
        while not placement_confirmed and not cancelled:
            preview_piece(board, piece, x, y, player_color)
            listener.join(0.1)  # Rafraîchit l'écran

    if cancelled:
        return None, None
    return x, y

# Place une pièce sur le plateau
def place_piece(board, piece, x, y, player_color):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 1:
                board[x + i][y + j] = player_color

# Vérifie si une pièce peut être placée
def can_place_piece(board, piece, x, y, player_color, first_move):
    rows, cols = len(piece), len(piece[0])
    board_rows, board_cols = len(board), len(board[0])
    corner_touch = False

    if x + rows > board_rows or y + cols > board_cols:
        return False

    for i in range(rows):
        for j in range(cols):
            if piece[i][j] == 1:
                if board[x + i][y + j] != 0:  # Occupation
                    return False
    return True

# Jeu principal
def main():
    print("Bienvenue dans Blokus !")
    board_size = 10
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    pieces = generate_pieces()
    players = ["blue", "yellow"]
    current_player = 0

    while True:
        player_color = players[current_player]
        print(f"\nC'est le tour du joueur {player_color.capitalize()} :")
        display_board(board)
        player_pieces = pieces[player_color]

        # Affichage des pièces disponibles
        for i, piece in enumerate(player_pieces):
            print(f"Pièce {i}:")
            for row in piece:
                print(" ".join(f"{COLOR_CODES[player_color]}■{COLOR_CODES['reset']}" if cell else " " for cell in row))

        while True:
            try:
                piece_index = int(input("Entrez le numéro de la pièce à placer ou tapez '-1' pour passer : "))
                if piece_index == -1:
                    print(f"{player_color.capitalize()} passe son tour.")
                    break

                piece = player_pieces[piece_index]
                x, y = simulate_placement(board, piece, player_color)

                if x is None or y is None:
                    print("Placement annulé.")
                elif can_place_piece(board, piece, x, y, player_color, first_move=True):
                    place_piece(board, piece, x, y, player_color)
                    pieces[player_color].pop(piece_index)
                    break
                else:
                    print("Placement invalide. Réessayez.")
            except (ValueError, IndexError):
                print("Entrée invalide. Réessayez.")

        current_player = (current_player + 1) % len(players)

        if all(len(pieces[player]) == 0 for player in players):
            print("Partie terminée !")
            break

if __name__ == "__main__":
    main()
