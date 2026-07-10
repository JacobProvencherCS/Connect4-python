# TODO : verify that my code works on edge cases -> enumerate possible edge cases to cover !

from _collections_abc import Callable
from collections import defaultdict

# Renaming types for readability
Column = list[int]
Board = list[Column]


def get_next_index(col: Column) -> int:
    """
    Méthode qui retourne l'indice de la prochaine cellule vide.
    :param col:
    :return: Un entier représentant l'indice de la prochaine cellule vide, celle du dessus.
    """
    for i, v in enumerate(col, start=1):
        if v == 0:
            return i
    return 0


def is_all_the_same(lst: Column):
    return all(n == lst[0] and lst[0] != 0 for n in lst)


def full_transpose(grid: Board) -> Board:
    return [list(col) for col in zip(*grid)]


def vertical_check(grid: Board) -> int:
    for col in grid:
        if 0 <= (slider_buffer := len(col) - 4) <= 3:
            for i in range(slider_buffer):
                window: Column = col[i:i + 4]
                if is_all_the_same(window):
                    return col[i]

    return False


class Connect4:

    def __init__(self, player1: str, player2: str) -> None:

        self.diag_lut = None
        self.player1: str = player1
        self.player2: str = player2
        self.endings_LUT: dict[int, str] = {
            1: "player 1 wins",
            2: "player 2 wins",
            3: "nulle",
        }
        self.grid: list[list] = [[] for _ in range(7)]
        self.initialize_diag_lut()
        self.checks: list[Callable[[Board], int]] = [vertical_check,
                                                     self.horizontal_check,
                                                     self.positive_diagonal_check,
                                                     self.negative_diagonal_check]

    def initialize_diag_lut(self) -> None:
        """
        Méthode qui initialise le dictionnaire des positions utilisé pour la
        méthode ``half-transpose``.

        :return: None
        """
        self.diag_lut = defaultdict(list)
        for n in range(-5, 6):
            for a, b in [(j, i) for j in range(6) for i in range(6)]:
                if b - a == n:
                    self.diag_lut[n].append((a, b))
        for n in range(6):
            self.diag_lut[n - 6].append((6, n))

    def set_token(self, col: int, player: int) -> bool:
        """
        Méthode permettant de placer un jeton dans la colonne ``col``.

        :param col: L'indice de la colonne visée.
        :param player: Le joueur qui place le jeton.
        :return: Indique si le placement a réussi.
        """
        if not (1 <= col <= 7):
            return False

        valid_move = False

        if index := get_next_index(self.grid[col - 1]):
            self.grid[col - 1][index - 1] = player
            valid_move = True

        return valid_move

    def __str__(self) -> str:
        """
        Appelée lors de l'utilisation de ``print``.
        :return: Une chaîne de caractères
        """
        return "\n".join(
            [" ".join(map(str, line)) for line in list(reversed(full_transpose(self.grid)))])

    def add_padding(self) -> None:
        """
        Remplit la grille avec des ``zeros``.
        :return: Aucun
        """
        for col in self.grid:
            col.extend([0] * max(0, 7 - len(col)))

    def half_transpose(self, grid: Board) -> Board:
        """
        Méthode qui retourne la grille avec une rotation de 45 degrée, de sorte à
        obtenir une liste de liste, où chaque sous-liste représente une diagonale
        contenant au moins quatre éléments.
        :param grid: Une liste de liste à transposer.
        :return: Une liste de liste, représentant chaque diagonale.
        """
        myList = []

        for indexes in self.diag_lut.values():
            another_list = []
            for j, i in indexes:
                another_list.append(grid[j][i])
            myList.append(another_list)

        final_list = [e for e in myList if not len(e) < 4]

        return final_list

    def is_winner(self, grid: Board) -> int:
        """
        Méthode qui vérifie si la grille passée en paramètre contient un joueur gagnant.
        Ainsi, la méthode vérifie si la grille contient quatre jetons à la suite, placé soit
        horizontalement, verticalement ou selon une diagonale.

        Issue possible :
        - 0 : partie pas terminée
        - 1 : joueur 1 gagne
        - 2 : joueur 2 gagne
        - 3 : partie nulle

        :param grid: Une liste de liste à vérifier.
        :return: Un entier, représentant l'issue de la partie.
        """

        for check in self.checks:
            if winner := check(grid):
                return winner

        return False

    def horizontal_check(self, grid: Board) -> int:
        """
        Méthode vérifiant si `grid` contient quatre jetons placés horizontalement
        à la suite.
        :param grid: Une liste de liste à vérifier
        :return: Un entier, représentant l'issue de la partie.
        """
        self.add_padding()
        return vertical_check(full_transpose(grid))

    def positive_diagonal_check(self, grid: Board) -> int:
        """
        Méthode vérifiant si `grid` contient quatre jetons placés diagonalement
        à la suite.
        :param grid: Une liste de liste à vérifier
        :return: Un entier, représentant l'issue de la partie.
        """
        return vertical_check(self.half_transpose(grid))

    def negative_diagonal_check(self, grid: Board) -> int:
        """
        Méthode vérifiant si `grid` contient quatre jetons placés diagonalement
        à la suite.
        :param grid: Une liste de liste à vérifier
        :return: Un entier, représentant l'issue de la partie.
        """
        return self.positive_diagonal_check(list(reversed(grid)))

    def mainloop(self) -> None:
        """
        Boucle d'entrée principale du jeu
        :return: Aucun.
        """
        player_turn: int = 1

        while not (finished := self.is_winner(self.grid)):

            print(f"Joueur {player_turn} à jouer...")
            col_input = int(input("Enter a column number: "))

            if self.set_token(col_input, player_turn):
                print(self)
                player_turn: int = player_turn % 2 + 1

            else:
                print("Invalid input. Please try again.")

        print(f"L'issue de la partie est {self.endings_LUT[finished]}")


if __name__ == "__main__":
    game = Connect4("Jacob", "Melodie")
    game.mainloop()
