import os
from pynput import keyboard

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
    # Les 21 pièces fournies
    return {
        1: [(0, 0)],  # Monomino
        2: [(0, 0), (1, 0)],  # Domino
        3: [(0, 0), (1, 0), (2, 0)],  # Tromino ligne
        4: [(0, 0), (1, 0), (0, 1)],  # Tromino L
        5: [(0, 0), (1, 0), (2, 0), (3, 0)],  # Tetromino ligne
        6: [(0, 0), (0, 1), (0, 2), (1, 0)],  # Tetromino L inversé
        7: [(0, 0), (1, 0), (1, 1), (2, 0)],  # Tetromino T
        8: [(0, 0), (1, 0), (0, 1), (1, 1)],  # Tetromino carré
        9: [(0, 0), (1, 0), (1, 1), (2, 1)],  # Tetromino Z
        10: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Pentomino ligne
        11: [(0, 0), (1, 0), (2, 0), (3, 0), (3, -1)],  # Pentomino crochet inversé
        12: [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],  # Pentomino L
        13: [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)],  # Pentomino tour
        14: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)],  # Pentomino crochet
        15: [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1)],  # Pentomino crochet inversé
        16: [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],  # Pentomino T
        17: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # Pentomino L inversé avec extension
        18: [(0, 0), (0, 1), (1, 1), (2, 2), (1, 2)],  # Pentomino W
        19: [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],  # Pentomino F
        20: [(0, 0), (1, -1), (1, 0), (2, 0), (2, 1)],  # Pentomino W inversé
        21: [(0, 0), (1, 0), (1, 1), (1, -1), (2, 0)],  # Pentomino croix
    }

# Génère les pièces pour chaque joueur
def generate_pieces():
    piece_model = generate_piece_model()
    # Transformer les coordonnées en grilles 2D
    def piece_to_grid(piece):
        max_x = max([x for x, _ in piece])
        max_y = max([y for _, y in piece])
        grid = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for x, y in piece:
            grid[x][y] = 1
        return grid

    return {
        "blue": [piece_to_grid(piece) for piece in piece_model.values()],
        "yellow": [piece_to_grid(piece) for piece in piece_model.values()],
        "red": [piece_to_grid(piece) for piece in piece_model.values()],
        "green": [piece_to_grid(piece) for piece in piece_model.values()],
    }

# Convertit un index en coordonnée (ligne ou colonne)
def index_to_coordinate(index):
    if index < 10:
        return str(index)
    return chr(index - 10 + ord("A"))

# Affiche le plateau de jeu
def display_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoyer l'écran
    # En-têtes des colonnes
    column_headers = [index_to_coordinate(i) for i in range(len(board[0]))]
    print("   " + " ".join(column_headers))
    # Affichage des lignes avec en-têtes de lignes
    for i, row in enumerate(board):
        row_header = index_to_coordinate(i)
        print(f"{row_header:2} " + " ".join(
            f"{COLOR_CODES[cell]}■{COLOR_CODES['reset']}" if cell in COLOR_CODES else "." for cell in row
        ))

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

# Vérifie si une pièce peut être placée
def can_place_piece(board, piece, x, y, player_color, first_move):
    rows, cols = len(board), len(board[0])
    corner_touch = False  # Vérifie le contact par un coin
    edge_touch = False  # Vérifie le contact par les côtés

    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 1:
                nx, ny = x + i, y + j

                # Vérifier si la pièce dépasse les limites du plateau
                if not (0 <= nx < rows and 0 <= ny < cols):
                    return False

                # Vérifier si la case est déjà occupée
                if board[nx][ny] != 0:
                    return False

                # Vérifier le contact par un coin
                for cx, cy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if 0 <= nx + cx < rows and 0 <= ny + cy < cols:
                        if board[nx + cx][ny + cy] == player_color:
                            corner_touch = True

                # Vérifier le contact par les côtés (empêcher pour les pièces de la même couleur)
                for ex, ey in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= nx + ex < rows and 0 <= ny + ey < cols:
                        if board[nx + ex][ny + ey] == player_color:
                            edge_touch = True

    if first_move:
        # Vérifiez que la pièce occupe l'un des coins attribués au joueur
        if player_color == "blue":
            return any((x + dx, y + dy) == (0, 0) for dx, row in enumerate(piece) for dy, val in enumerate(row) if val)
        elif player_color == "yellow":
            return any((x + dx, y + dy) == (0, cols - 1) for dx, row in enumerate(piece) for dy, val in enumerate(row) if val)
        elif player_color == "red":
            return any((x + dx, y + dy) == (rows - 1, 0) for dx, row in enumerate(piece) for dy, val in enumerate(row) if val)
        elif player_color == "green":
            return any((x + dx, y + dy) == (rows - 1, cols - 1) for dx, row in enumerate(piece) for dy, val in enumerate(row) if val)


    # Une pièce est valide si elle touche une pièce de la même couleur par un coin,
    # sans toucher une pièce de la même couleur par un côté
    return corner_touch and not edge_touch

# Place une pièce sur le plateau
def place_piece(board, piece, x, y, player_color):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 1:
                board[x + i][y + j] = player_color

# Menu pour sélectionner le nombre de joueurs
def get_players():
    while True:
        try:
            num_players = int(input("Entrez le nombre de joueurs (2 à 4) : "))
            if 2 <= num_players <= 4:
                colors = ["blue", "yellow", "red", "green"]
                return colors[:num_players]
            else:
                print("Veuillez entrer un nombre entre 2 et 4.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")

# Fonction principale du jeu
def main():
    print("Bienvenue dans Blokus !")
    board_size = 20
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    pieces = generate_pieces()  # Générer les pièces pour chaque joueur
    players = get_players()  # Obtenir le nombre de joueurs
    current_player = 0
    first_moves = {player: True for player in players}  # Suivi des premiers mouvements pour chaque joueur

    while True:
        # Déterminer le joueur actuel
        player_color = players[current_player]
        print(f"\nC'est le tour du joueur {player_color.capitalize()} :")
        display_board(board)  # Afficher le plateau de jeu
        player_pieces = pieces[player_color]

        while True:
            try:
                # Afficher les pièces disponibles pour le joueur actuel
                print(f"Joueur {player_color.capitalize()}, voici vos pièces disponibles :")
                for i, piece in enumerate(player_pieces):
                    print(f"Pièce {i}:")
                    for row in piece:
                        print(" ".join(f"{COLOR_CODES[player_color]}■{COLOR_CODES['reset']}" if cell else " " for cell in row))

                # Demander au joueur de choisir une pièce ou de passer son tour
                piece_input = input("Entrez le numéro de la pièce à placer ou 'P' pour passer votre tour : ").strip()

                # Gérer le passage de tour
                if piece_input.upper() == "P":
                    print(f"{player_color.capitalize()} a passé son tour.")
                    break

                # Récupérer la pièce choisie
                piece_index = int(piece_input)
                piece = player_pieces[piece_index]
                print("Simulation interactive pour le placement de la pièce...")

                # Simulation interactive pour le placement de la pièce
                x, y = simulate_placement(board, piece, player_color)

                # Vérifie si le placement est valide
                if x is not None and y is not None:  # Si le placement n'est pas annulé
                    if can_place_piece(board, piece, x, y, player_color, first_moves[player_color]):
                        place_piece(board, piece, x, y, player_color)  # Placer la pièce
                        player_pieces.pop(piece_index)  # Retirer la pièce placée
                        first_moves[player_color] = False  # Le joueur a effectué son premier mouvement
                        break
                    else:
                        print("Placement invalide. Réessayez.")

            except (ValueError, IndexError):
                print("Entrée invalide. Réessayez.")

        # Passer au joueur suivant
        current_player = (current_player + 1) % len(players)

        # Vérifier si le jeu est terminé
        if all(len(pieces[player]) == 0 for player in players):
            print("\nFin de la partie!")
            break


if __name__ == "__main__":
    main()
