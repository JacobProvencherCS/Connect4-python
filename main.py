







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
            print(grid)
            player_turn = player_turn % 2 + 1
        else:
            print("Invalid input. Please try again.")

    print(f"L'issue de la partie est {endings_LUT[gamestate]}")


def set_token(grid: list[list[int]], col: int, player: int):

    valid_move = False

    if 0 <= len(grid[col - 1]) < 7:
        grid[col - 1].append(player)
        valid_move = True

    return valid_move

def beauty_print(grid: list[list[int]]) -> str: #todo
    pass

def is_winner(grid: list[list[int]]) -> bool:
    return False


if __name__ == "__main__":
    mainloop()
