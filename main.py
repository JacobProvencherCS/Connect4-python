# TODO : is_winner (and related functions needs to return 0, 1, 2 or 3)
# TODO : transfer to OOP code development

from pprint import pprint

endings_LUT = {
    1: "player 1 wins",
    2: "player 2 wins",
    3: "nulle",
}


def mainloop() -> None:
    grid = [[] for _ in range(7)]
    player_turn = 1

    while not (gamestate := is_winner(grid)):
        col_input = int(input("Enter a column number: "))
        if set_token(grid, col_input, player_turn):
            print(beauty_grid(grid))
            player_turn = player_turn % 2 + 1
        else:
            print("Invalid input. Please try again.")

    print(f"L'issue de la partie est {endings_LUT[gamestate]}")


def get_next_index(col: list[int]) -> int | None:
    for i, v in enumerate(col, start=1):
        if v == 0:
            return i

    return 0


def set_token(grid: list[list[int]], col: int, player: int):
    valid_move = False

    if index := get_next_index(grid[col - 1]):
        grid[col - 1][index - 1] = player
        valid_move = True

    return valid_move


def beauty_grid(grid: list[list[int]]) -> str:
    return "\n".join([" ".join(map(str, line)) for line in list(reversed(transpose(add_padding(grid))))])


def add_padding(grid: list[list[int]]) -> list[list[int]]:
    for col in grid:
        col.extend([0] * max(0, 7 - len(col)))

    return grid


def is_all_the_same(lst: list[int]):
    return all(n == lst[0] and lst[0] != 0 for n in lst)


def transpose(grid: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*grid)]


def is_winner(grid: list[list[int]]) -> int:
    verifications = [horizontal_check,
                     vertical_check,
                     pos_diag_check,
                     neg_diag_check]

    for verif in verifications:
        if winner := verif(grid):
            return winner

    return False


def vertical_check(grid: list[list[int]]) -> int:
    for col in grid:
        if 0 <= (slider_buffer := len(col) - 4) <= 3:
            for i in range(slider_buffer):
                if is_all_the_same(col[i:i + 4]):
                    return col[i]

    return False


def horizontal_check(grid: list[list[int]]) -> int:
    return vertical_check(transpose(add_padding(grid)))


def pos_diag_check(grid: list[list[int]]) -> int:
    for j in range(4):
        for i in range(3):

            diag_values = [winner_player := grid[j][i],
                           grid[j + 1][i + 1],
                           grid[j + 2][i + 2],
                           grid[j + 3][i + 3]]

            if is_all_the_same(diag_values):
                return winner_player

    return False


def neg_diag_check(grid: list[list[int]]) -> int:
    return pos_diag_check(list(reversed(grid)))


if __name__ == "__main__":
    mainloop()
