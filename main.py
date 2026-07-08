from collections import defaultdict


class Connect4:

    def __init__(self, player1: str, player2: str) -> None:

        self.diag_lut = None
        self.player1 = player1
        self.player2 = player2
        self.endings_LUT = {
            1: "player 1 wins",
            2: "player 2 wins",
            3: "nulle",
        }
        self.grid = [[] for _ in range(7)]
        self.initialize_diag_lut()

    def initialize_diag_lut(self) -> None:
        self.diag_lut = defaultdict(list)
        for n in range(-5, 6):
            for a, b in [(j, i) for j in range(6) for i in range(6)]:
                if b - a == n:
                    self.diag_lut[n].append((a, b))
        for n in range(6):
            self.diag_lut[n - 6].append((6, n))

    def set_token(self, grid: list[list[int]], col: int, player: int):
        if not (1 <= col <= 7):
            return False

        valid_move = False

        if index := self.get_next_index(grid[col - 1]):
            grid[col - 1][index - 1] = player
            valid_move = True

        return valid_move

    def __str__(self) -> str:
        return "\n".join(
            [" ".join(map(str, line)) for line in list(reversed(self.full_transpose(self.grid)))])

    def add_padding(self) -> None:
        for col in self.grid:
            col.extend([0] * max(0, 7 - len(col)))

    def get_next_index(self, col: list[int]) -> int:
        for i, v in enumerate(col, start=1):
            if v == 0:
                return i
        return 0

    def is_all_the_same(self, lst: list[int]):
        return all(n == lst[0] and lst[0] != 0 for n in lst)

    def full_transpose(self, grid: list[list[int]]) -> list[list[int]]:
        return [list(col) for col in zip(*grid)]

    def half_transpose(self, grid: list[list[int]]) -> list[list[int]]:

        myList = []

        for indexes in self.diag_lut.values():
            another_list = []
            for j, i in indexes:
                another_list.append(grid[j][i])
            myList.append(another_list)

        final_list = [e for e in myList if not len(e) < 4]

        return final_list

    def is_winner(self, grid: list[list[int]]) -> int:
        verifications = [self.horizontal_check,
                         self.vertical_check,
                         self.pos_diag_check,
                         self.neg_diag_check]

        for verif in verifications:
            if winner := verif(grid):
                return winner

        return False

    def vertical_check(self, grid: list[list[int]]) -> int:
        for col in grid:
            if 0 <= (slider_buffer := len(col) - 4) <= 3:
                for i in range(slider_buffer):  # slide the sliding window
                    window = col[i:i + 4]
                    if self.is_all_the_same(window):
                        return col[i]
        return False

    def horizontal_check(self, grid: list[list[int]]) -> int:
        self.add_padding()
        return self.vertical_check(self.full_transpose(grid))

    def pos_diag_check(self, grid: list[list[int]]) -> int:
        return self.vertical_check(self.half_transpose(grid))

    def neg_diag_check(self, grid: list[list[int]]) -> int:
        return self.pos_diag_check(list(reversed(grid)))

    def mainloop(self) -> None:
        player_turn = 1

        while not (finished := self.is_winner(self.grid)):
            print(f"Joueur {player_turn} à jouer...")
            col_input = int(input("Enter a column number: "))
            if self.set_token(self.grid, col_input, player_turn):
                print(self)
                player_turn = player_turn % 2 + 1
            else:
                print("Invalid input. Please try again.")

        print(f"L'issue de la partie est {self.endings_LUT[finished]}")


if __name__ == "__main__":
    game = Connect4("Jacob", "Melodie")
    game.mainloop()
