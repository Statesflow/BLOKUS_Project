# Blokus Python Game

Bienvenue dans le jeu **Blokus** en Python ! Ce projet implémente une version interactive du célèbre jeu de Blokus, jouable directement dans le terminal.

## Pré-requis

Assurez-vous que Python est installé sur votre machine. Ce projet utilise **Python 3.6** ou une version ultérieure.

### Dépendances

Le projet nécessite la bibliothèque suivante :

- **`pynput`** : pour capturer les entrées clavier lors de la simulation interactive.

Si `pynput` n'est pas installé sur votre machine, vous pouvez l'ajouter en suivant les instructions ci-dessous.

`pip install pynput`

Si vous utilisez Python 3 et que pip n'est pas configuré, essayez :

`python3 -m pip install pynput`

## Installation

1. **Clonez ou téléchargez ce projet** :
   ```bash
   git clone https://github.com/Statesflow/BLOKUS_Project

2. **Lancer le jeu**
`python main.py`

## Comment jouer ?

1. **Sélectionnez le nombre de joueurs :**
Lors du démarrage, le jeu vous demandera le nombre de joueurs (entre 2 et 4). Entrez un nombre valide pour commencer la partie.

2. **Tour des joueurs :**
Chaque joueur joue à son tour.
Lors de votre tour, le jeu affichera les pièces disponibles avec leurs numéros.

3. **Choisissez une pièce :**
Entrez le numéro de la pièce que vous souhaitez placer.
Une fois la pièce sélectionnée, utilisez les touches suivantes pour déplacer ou valider la position de la pièce :
Flèche haut : Déplacer vers le haut.
Flèche bas : Déplacer vers le bas.
Flèche gauche : Déplacer vers la gauche.
Flèche droite : Déplacer vers la droite.
Entrée : Valider le placement de la pièce.
Échap : Annuler le placement et revenir au menu de sélection des pièces.

4. **Règles spéciales :**
La première pièce de chaque joueur doit être placée dans l'un des coins attribués à leur couleur :
Bleu : Coin supérieur gauche (0, 0)
Jaune : Coin supérieur droit (0, dernière colonne)
Rouge : Coin inférieur gauche (dernière ligne, 0)
Vert : Coin inférieur droit (dernière ligne, dernière colonne)
Les pièces suivantes doivent toucher une pièce de la même couleur par un coin, mais ne doivent pas toucher une pièce de la même couleur par les côtés.
Les pièces de couleurs différentes peuvent se toucher par les côtés.

5. **Fin de la partie :**
Le jeu se termine lorsqu'aucun joueur ne peut placer de pièce supplémentaire. Le gagnant est déterminé selon les règles classiques de Blokus

