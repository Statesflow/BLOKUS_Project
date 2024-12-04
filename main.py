import random

PIECES = [
    [["*"]],
    [["*", "*"]],
    [["*", "*", "*"]],
    [["*", "."], ["*", "*"]],
    [["*", "*", "*", "*"]],
    [["*", "*"], ["*", "*"]],
    [["*", ".", "."], ["*", "*", "*"]],
    [[".", "*", "."], ["*", "*", "*"]],
    [["*", "*", "."], [".", "*", "*"]],
    [["*", "*", "*", "*", "*"]],
    [["*", ".", "."], ["*", "*", "*"]],
    [["*", "*", "*"], [".", "*", "*"]],
    [[".", "*", "."], ["*", "*", "*"]],
    [["*", "*", "."], ["*", "*", "*"]],
    [["*", "*", "."], [".", "*", "*"]],
    [["*", ".", "."], ["*", "*", "*"]],
    [["*", "*", "*"], [".", "*", "*"]],
    [[".", "*", "."], ["*", "*", "*"]],
    [["*", "*", "*"], [".", "*", "*"]],
    [["*", "*", "."], [".", "*", "*"]],
    [["*", ".", ".", "*"], [".", "*", "*"]],
    [["*", "*", "*"], [".", "*", "."]],
]

def generate_grid(size):
    """Génère une grille vide."""
    return [["." for _ in range(size)] for _ in range(size)]

def print_grid(grid):
    """Affiche la grille."""
    for row in grid:
        print(" ".join(row))
    print()

def generate_player_pieces(player_id):
    """Génère les pièces d'un joueur, avec son numéro à la place des *."""
    def replace_with_player_id(piece):
        return [[str(player_id) if cell == "*" else cell for cell in row] for row in piece]
    return [replace_with_player_id(piece) for piece in PIECES]

def rotate_piece(piece, rotation):
    """Fait pivoter une pièce de 90°, 180°, ou 270°."""
    if rotation == 90:
        return [list(row) for row in zip(*piece[::-1])]
    elif rotation == 180:
        return [row[::-1] for row in piece[::-1]]
    elif rotation == 270:
        return [list(row) for row in zip(*piece)][::-1]
    return piece

def color_piece(piece, player):
    """Colorie une pièce selon le joueur."""
    colors = {1: "\033[94m", 2: "\033[91m", 3: "\033[93m", 4: "\033[92m"}  # Bleu, rouge, jaune, vert
    reset = "\033[0m"
    color = colors[player]
    return [[color + cell + reset if cell.isdigit() else "." for cell in row] for row in piece]

def print_piece(piece, player):
    """Affiche une pièce colorée."""
    colored_piece = color_piece(piece, player)
    for row in colored_piece:
        print(" ".join(row))
    print()

def place_piece(grid, piece, x, y, player):
    """Place une pièce sur la grille."""
    for i, row in enumerate(piece):
        for j, cell in enumerate(row):
            if cell.isdigit():
                grid[x + i][y + j] = cell

def can_place_piece(grid, piece, x, y, player):
    """Vérifie si une pièce peut être placée selon les règles du Blokus."""
    size = len(grid)
    touching_corner = False
    for i, row in enumerate(piece):
        for j, cell in enumerate(row):
            if cell.isdigit():
                nx, ny = x + i, y + j
                if not (0 <= nx < size and 0 <= ny < size) or grid[nx][ny] != ".":
                    return False
                # Vérifier les voisins
                neighbors = [
                    (nx - 1, ny), (nx + 1, ny), (nx, ny - 1), (nx, ny + 1)
                ]
                for nx2, ny2 in neighbors:
                    if 0 <= nx2 < size and 0 <= ny2 < size and grid[nx2][ny2] == str(player):
                        return False
                # Vérifier les coins
                corners = [
                    (nx - 1, ny - 1), (nx - 1, ny + 1), (nx + 1, ny - 1), (nx + 1, ny + 1)
                ]
                for cx, cy in corners:
                    if 0 <= cx < size and 0 <= cy < size and grid[cx][cy] == str(player):
                        touching_corner = True
    return touching_corner

def play_game(size):
    """Lance le jeu Blokus avec les règles appropriées."""
    grid = generate_grid(size)
    players = [1, 2, 3, 4]
    turn = 0

    # Générer les pièces pour chaque joueur
    player_pieces = {player: generate_player_pieces(player) for player in players}
    print("Bienvenue dans Blokus !")
    print_grid(grid)

    while True:
        current_player = players[turn % len(players)]
        print(f"Joueur {current_player}, c'est votre tour.")

        # Afficher les pièces restantes
        print(f"Pièces restantes pour le joueur {current_player} :")
        display_pieces = player_pieces[current_player]
        for i, piece in enumerate(display_pieces, start=1):
            print(f"Pièce {i}:")
            print_piece(piece, current_player)

        # Sélectionner une pièce
        while True:
            try:
                piece_index = int(input(f"Choisissez une pièce (1-{len(display_pieces)}) : ")) - 1
                if 0 <= piece_index < len(display_pieces):
                    piece = display_pieces.pop(piece_index)
                    break
                print("Sélection invalide. Essayez encore.")
            except ValueError:
                print("Entrée invalide. Essayez encore.")

        # Rotation de la pièce
        while True:
            try:
                rotation = int(input("Entrez une rotation (0, 90, 180, 270) : "))
                if rotation in [0, 90, 180, 270]:
                    piece = rotate_piece(piece, rotation)
                    break
                print("Rotation invalide. Essayez encore.")
            except ValueError:
                print("Entrée invalide. Essayez encore.")

        # Placer la pièce
        while True:
            try:
                x = int(input(f"Entrez la ligne pour placer la pièce (0-{size - 1}) : "))
                y = int(input(f"Entrez la colonne pour placer la pièce (0-{size - 1}) : "))
                if can_place_piece(grid, piece, x, y, current_player):
                    place_piece(grid, piece, x, y, current_player)
                    break
                print("Placement invalide. Essayez encore.")
            except ValueError:
                print("Entrée invalide. Essayez encore.")

        print_grid(grid)
        turn += 1

        # Fin du jeu si tous les joueurs passent
        if all(len(player_pieces[p]) == 0 for p in players):
            print("Partie terminée !")
            break

# Lancer le jeu
play_game(20)
