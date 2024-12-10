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

# Convertit une coordonnée (numérique ou alphabétique) en indice
def convert_coordinate(coord):
    if coord.isdigit():
        return int(coord)
    return ord(coord.upper()) - ord("A") + 10

# Convertit un index en coordonnée (ligne ou colonne)
def index_to_coordinate(index):
    if index < 10:
        return str(index)
    return chr(index - 10 + ord("A"))

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
                # Vérification du coin pour le placement autorisé
                if first_move and not ((x + i == 0 and y + j == 0) or 
                                       (x + i == 0 and y + j == board_cols - 1) or 
                                       (x + i == board_rows - 1 and y + j == 0) or 
                                       (x + i == board_rows - 1 and y + j == board_cols - 1)):
                    return False
                # Contact par un coin
                if (
                    (x + i - 1 >= 0 and y + j - 1 >= 0 and board[x + i - 1][y + j - 1] == player_color) or
                    (x + i - 1 >= 0 and y + j + 1 < board_cols and board[x + i - 1][y + j + 1] == player_color) or
                    (x + i + 1 < board_rows and y + j - 1 >= 0 and board[x + i + 1][y + j - 1] == player_color) or
                    (x + i + 1 < board_rows and y + j + 1 < board_cols and board[x + i + 1][y + j + 1] == player_color)
                ):
                    corner_touch = True

    return corner_touch or first_move

# Place une pièce sur le plateau
def place_piece(board, piece, x, y, player_color):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 1:
                board[x + i][y + j] = player_color

# Affiche le plateau de jeu avec des coordonnées adaptées
def display_board(board):
    column_headers = [index_to_coordinate(i) for i in range(len(board[0]))]
    row_headers = [index_to_coordinate(i) for i in range(len(board))]
    print("   " + "  ".join(column_headers))
    for i, row in enumerate(board):
        print(f"{row_headers[i]:2} " + "  ".join(
            f"{COLOR_CODES[cell]}■{COLOR_CODES['reset']}" if cell in COLOR_CODES else "."
            for cell in row
        ))

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

# Jeu principal
def main():
    print("Bienvenue dans Blokus !")
    board_size = 20
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    pieces = generate_pieces()
    players = get_players()
    current_player = 0
    first_moves = {player: True for player in players}

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
            piece_input = input("Entrez le numéro de la pièce à placer ou tapez 'P' pour passer votre tour : ").strip()
    
            # Vérifier si l'utilisateur veut passer son tour
            if piece_input.upper() == "P":
                print(f"{player_color.capitalize()} a passé son tour.")
                break

            try:
                # Convertir l'entrée en entier pour le numéro de pièce
                piece_index = int(piece_input)
                piece = player_pieces[piece_index]
                
                # Demander les coordonnées
                if first_moves:
                    print("Veuillez entrez votre 1r mouvement rappel : \n bleu = 00 ; jaune = 0J ; roouge = JJ ; vert = J0")
                    coords = input("Entrez les coordonnées de la votre 1re pièce: ").strip()
                else :
                    coords = input("Entrez les coordonnées de la pièce (ex : 00, A1) : ").strip()
                row = convert_coordinate(coords[0])
                col = convert_coordinate(coords[1:])
                if can_place_piece(board, piece, row, col, player_color, first_moves[player_color]):
                    place_piece(board, piece, row, col, player_color)
                    pieces[player_color].pop(piece_index)
                    first_moves[player_color] = False
                    break
                else:
                    print("Placement invalide. Réessayez.")
            except (ValueError, IndexError):
                print("Entrée invalide. Réessayez.")

        current_player = (current_player + 1) % len(players)

        # Fin de la partie si toutes les pièces sont placées ou impossibles à placer
        if all(len(pieces[player]) == 0 for player in players):
            break

    print("\nPartie terminée !")

if __name__ == "__main__":
    main()
